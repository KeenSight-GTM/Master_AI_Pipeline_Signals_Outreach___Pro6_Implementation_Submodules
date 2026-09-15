"""Local design-test export only. No CRM mutation, transport or sending.

The caller supplies an authenticated principal ID resolved outside this module;
this fixture uses the trusted actors registry instead of an identity provider.
"""
from dataclasses import dataclass
from pathlib import Path
import os
from .completion import export_payload
from .engine import digest, require

@dataclass(frozen=True)
class LocalExportResult:
    path: str
    payload_hash: str
    reused: bool
    send_allowed: bool = False

class LocalPreviewExporter:
    def __init__(self,bundle,output_directory: Path):
        self.bundle=bundle
        self.directory=Path(output_directory).resolve()

    def export(self,gate_id: str,*,principal_id: str,at: str,idempotency_key: str) -> LocalExportResult:
        b=self.bundle;gate=b.row('gates',gate_id);pkg=b.row('packages',gate['package']['package_id'])
        b.require_actor(principal_id,gate['tenant_id'],'EXPORT')
        require(b.row('runs',pkg['run_id'])['mode']=='DESIGN_TEST','LIVE_EXPORT_NOT_IMPLEMENTED')
        destination=b.reg('destinations',gate['destination_id'])
        require(destination['kind']=='LOCAL_PREVIEW' and destination['fixture_only'],'REMOTE_EXPORT_NOT_IMPLEMENTED')
        b.validate_gate(gate,at);require(gate['decision']=='ALLOW','EXPORT_GATE_BLOCKED')
        data=export_payload(pkg,destination,gate['recipient_key'])
        key=digest({'tenant':gate['tenant_id'],'destination':destination['destination_id'],'idempotency_key':idempotency_key}).split(':')[1]
        self.directory.mkdir(parents=True,exist_ok=True)
        path=self.directory/(key+'.json')
        # O_EXCL prevents an accidental overwrite or a second payload for a key.
        # Recovery of incomplete local writes remains fail-closed, not silent resend.
        try:fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except FileExistsError:
            require(path.is_file() and not path.is_symlink() and path.read_bytes()==data,'IDEMPOTENCY_PAYLOAD_CONFLICT')
            return LocalExportResult(str(path),digest(data),True)
        with os.fdopen(fd,'wb') as f:
            f.write(data);f.flush();os.fsync(f.fileno())
        return LocalExportResult(str(path),digest(data),False)
