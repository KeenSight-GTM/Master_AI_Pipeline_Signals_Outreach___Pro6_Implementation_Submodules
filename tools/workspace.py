#!/usr/bin/env python3
"""Local workspace launcher; NOT a generic ModuleRequest runner or hosted API.

Existing commands run in separate processes against one authoritative source tree.
Normal checks do not fetch URLs, invoke providers, or send messages. Dependencies
must be installed separately. Former audit failures are mandatory regression gates.
"""
from __future__ import annotations

import argparse
from dataclasses import dataclass
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import subprocess
import sys
import time

ROOT = Path(__file__).resolve().parents[1]


@dataclass(frozen=True)
class Step:
    name: str
    args: tuple[str, ...]
    cwd: Path
    expected_exit: int = 0


def environment() -> dict[str, str]:
    """Provide local modules without installing a second copy of the source."""
    env = dict(os.environ)
    paths = [str(ROOT / "collector/src"), str(ROOT / "canonical")]
    if env.get("PYTHONPATH"):
        paths.append(env["PYTHONPATH"])
    env["PYTHONPATH"] = os.pathsep.join(paths)
    env["KEENSIGHT_BASELINE"] = str(ROOT)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    return env


def external_output(value: str | None, label: str) -> Path:
    """Keep generated databases, artifacts and run logs outside the source tree."""
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    out = (Path(value).expanduser() if value else
           ROOT.parent / "keensight-runs" / f"{label}-{stamp}").resolve()
    if out == ROOT or out.is_relative_to(ROOT):
        raise ValueError("Choose an output directory outside keensight-ai-pipeline.")
    out.mkdir(parents=True, exist_ok=True)
    return out


def run_steps(steps: list[Step], output: Path, timeout: int) -> int:
    output.mkdir(parents=True, exist_ok=True)
    entries: list[dict[str, object]] = []
    failed = False
    env = environment()
    for index, step in enumerate(steps, 1):
        command = [sys.executable, *step.args]
        print(f"[{index}/{len(steps)}] {step.name}", flush=True)
        started = time.monotonic()
        try:
            proc = subprocess.run(command, cwd=step.cwd, env=env, text=True,
                                  capture_output=True, timeout=timeout)
            rc, stdout, stderr = proc.returncode, proc.stdout, proc.stderr
        except subprocess.TimeoutExpired as exc:
            def text(v: bytes | str | None) -> str:
                return v.decode(errors="replace") if isinstance(v, bytes) else (v or "")
            rc, stdout, stderr = 124, text(exc.stdout), text(exc.stderr) + "\nWorkspace timeout.\n"
        except OSError as exc:
            rc, stdout, stderr = 127, "", f"Could not start subprocess: {exc}\n"
        prefix = f"{index:02d}-{step.name}"
        (output / f"{prefix}.stdout.txt").write_text(stdout, encoding="utf-8")
        (output / f"{prefix}.stderr.txt").write_text(stderr, encoding="utf-8")
        ok = rc == step.expected_exit
        failed |= not ok
        row = {"name": step.name, "command": command, "cwd": str(step.cwd),
               "returncode": rc, "expected_returncode": step.expected_exit,
               "passed": ok, "elapsed_seconds": round(time.monotonic() - started, 3),
               "stdout_file": f"{prefix}.stdout.txt", "stderr_file": f"{prefix}.stderr.txt"}
        entries.append(row)
        (output / "run.json").write_text(json.dumps({
            "source_root": str(ROOT), "steps": entries,
            "all_expected_exit_codes": not failed,
            "scope": "LOCAL_WORKSPACE_COMMANDS_NOT_PRODUCTION_E2E"
        }, indent=2) + "\n", encoding="utf-8")
        tail = (stdout + stderr).strip().splitlines()[-4:]
        print("\n".join(tail), flush=True)
        print(f"  {'PASS' if ok else 'FAIL'} (exit {rc})", flush=True)
    print(f"Logs: {output}", flush=True)
    return 1 if failed else 0


def check_steps() -> list[Step]:
    return [
        Step("canonical-generation", ("generate.py", "--check"), ROOT / "canonical"),
        Step("canonical-validation", ("validate.py",), ROOT / "canonical"),
        Step("protocol-validation", ("validate_protocol.py",), ROOT / "protocol"),
        Step("product-design", ("validate_design.py",), ROOT / "product-design"),
        Step("implementation-plan", ("validate_plan.py",), ROOT / "implementation"),
    ]


def test_steps(output: Path) -> list[Step]:
    return [Step(name + "-tests", ("-m", "pytest", "-q", "-p", "no:cacheprovider",
                 f"--junitxml={output / (name + '.xml')}"), ROOT / name)
            for name in ("collector", "canonical", "protocol")] + [
        Step("workspace-tests", ("-m", "pytest", "-q", "-p", "no:cacheprovider",
             "tests/workspace", f"--junitxml={output / 'workspace.xml'}"), ROOT)] + [
        Step(name + "-requirements", ("-m", "pytest", "-q", "-p", "no:cacheprovider", "tests",
             f"--junitxml={output / (name + '.xml')}"), ROOT / "audits" / name)
        for name in ("poc", "iteration2")]


def parser() -> argparse.ArgumentParser:
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest="action", required=True)
    for name in ("check", "test", "verify", "demo", "journeys", "audit", "live-check"):
        c = sub.add_parser(name)
        c.add_argument("--output", help="Run output directory outside the source tree")
        c.add_argument("--timeout", type=int, default=300, help="Seconds per subprocess")
        if name == "journeys":
            c.add_argument("--journey", choices=["all-local"] + [f"J{i:02d}" for i in range(1,9)], default="all-local")
        if name == "audit":
            c.add_argument("suite", choices=["poc", "iteration2"])
            c.add_argument("--probes-only", action="store_true",
                           help="Record observations instead of enforcing the audit regression assertions")
    sub.add_parser("status")
    return p


def main(argv: list[str] | None = None) -> int:
    p = parser(); a = p.parse_args(argv)
    if a.action == "status":
        print((ROOT / "STATUS.json").read_text(encoding="utf-8")); return 0
    if a.timeout < 1:
        p.error("--timeout must be positive")
    try:
        out = external_output(a.output, a.action)
    except ValueError as exc:
        p.error(str(exc))
    if a.action == "check":
        steps = check_steps()
    elif a.action == "test":
        steps = test_steps(out)
    elif a.action == "verify":
        steps = check_steps() + test_steps(out)
    elif a.action == "demo":
        store = out / "demo-store"
        steps = [Step("demo", ("-m", "keensight_scrapling.cli", "demo", "--output", str(store)), ROOT),
                 Step("demo-check", ("-m", "keensight_scrapling.cli", "check",
                       str(store / "scan-bundle.json"), "--store", str(store)), ROOT)]
    elif a.action == "journeys":
        steps = [Step("journeys", ("walkthroughs/run_local_journeys.py", "--baseline", str(ROOT),
                  "--output", str(out / "journeys"), "--journey", a.journey), ROOT)]
    elif a.action == "audit":
        audit = ROOT / "audits" / a.suite
        if a.probes_only:
            # The POC probe script writes its reports relative to its own file. Execute
            # a temporary copy with an explicit shared-source override instead.
            import shutil
            name = "poc_probes.py" if a.suite == "poc" else "audit_probes.py"
            if a.suite == "poc":
                shutil.copyfile(audit / name, out / name)
                steps = [Step("poc-probes", (name,), out)]
            else:
                steps = [Step("iteration2-probes", (str(audit / name), "--output", str(out / "probe-results.json")), audit)]
        else:
            print("Audit regression suite: every requirement must pass; nonzero exits are not suppressed.", flush=True)
            steps = [Step(a.suite + "-requirements", ("-m", "pytest", "-q", "-p", "no:cacheprovider",
                     "tests", "--tb=short", f"--junitxml={out / 'audit.xml'}"), audit)]
    else:  # live-check must not silently pass through a missing-dependency skip
        check = subprocess.run([sys.executable, "-c", "from importlib.metadata import version; "
                               "assert version('scrapling') == '0.4.15'; "
                               "from scrapling.fetchers import FetcherSession"],
                               capture_output=True, text=True, env=environment())
        if check.returncode:
            print("Pinned Scrapling SDK unavailable. Install collector[live,test] first.\n" + check.stderr, file=sys.stderr)
            return 2
        steps = [Step("sdk-local-http", ("-m", "pytest", "-q", "-p", "no:cacheprovider",
                  "tests/test_live_integration.py"), ROOT / "collector")]
    return run_steps(steps, out, a.timeout)


if __name__ == "__main__":
    raise SystemExit(main())
