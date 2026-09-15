from importlib.resources import files
from .core import strict_json, CommandResult, ContractError

COMMANDS=tuple(x['command_id'] for x in strict_json(files('keensight_scrapling').joinpath('data/commands.json').read_text()))
assert len(COMMANDS)==38 and len(set(COMMANDS))==38


def complete_command_manifest(results: list[CommandResult]) -> list[CommandResult]:
    if any(r.command_id not in COMMANDS for r in results):
        raise ContractError('Unregistered command ID')
    emitted={r.command_id for r in results}
    # NOT_APPLICABLE is recorded, not falsely reported as execution success.
    return results+[CommandResult(c,'NOT_APPLICABLE',details={'reason':'Not selected for this capture/evaluation profile'}) for c in COMMANDS if c not in emitted]
