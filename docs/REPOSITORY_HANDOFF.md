# Local repository handoff

The ZIP contains ordinary editable source files. It is not an opaque archive embedded in a GitHub blob and requires no Git submodule initialization.

An optional `.bundle` artifact accompanies this delivery. It contains a local Git commit of this consolidated workspace. It is **not** proof of a GitHub push or merge.

```bash
git clone /path/to/keensight-ai-pipeline.bundle keensight-ai-pipeline
cd keensight-ai-pipeline
git log -1 --oneline
```

To integrate with the repository previously named in the conversation, use an authenticated local Git client and inspect its current branch first. The existing remote README/history must be preserved. For example, from an existing clone of the remote:

```bash
git fetch /path/to/keensight-ai-pipeline.bundle main:import/local-codebase
git switch -c import/full-codebase origin/main
git merge --allow-unrelated-histories --no-commit import/local-codebase
# Resolve any README conflict, inspect the full staged diff, and run tests.
git commit -m "Import consolidated KeenSight source, contracts, docs and audit tests"
git push -u origin import/full-codebase
```

There is no force-push, remote authentication, or remote repository mutation in the generated local tooling. Adding a merge commit and PR allows current remote work to be inspected before integration.

Before any public publication, review source rights, data permissions, histories, and any environment-specific values. The fixture examples are synthetic; provider credentials and raw production data are not required for the local tests. No new blanket software license is assigned by this assembly.
