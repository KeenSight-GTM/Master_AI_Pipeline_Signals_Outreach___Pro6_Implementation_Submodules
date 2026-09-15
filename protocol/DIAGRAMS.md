# Module flow and invocation model (editable Mermaid)

These diagrams describe the proposed wrappers; they do not show additional deployed services.

```mermaid
classDiagram
 class ModuleRequest {
  protocol_version
  request_id
  execution_id
  module_id
  operation
  context
  trace
  input_refs
  release_lock_ref
  parameters_ref
  idempotency_key
 }
 class ModuleResult {
  request_digest
  execution_status
  consumed_refs
  output_refs
  diagnostic_record_refs
  diagnostics
  usage
 }
 class RecordRef {
  record_id
  tenant_id
  schema_id
  schema_version
  content_digest
 }
 class ModuleHandler {
  execute(request) ModuleResult
 }
 class InvocationWrapper {
  validate_request()
  resolve_inputs()
  enforce_policy()
  record_start()
  call_handler()
  validate_and_commit_outputs()
  record_result()
 }
 class Diagnostic {
  code
  severity
  message
  record_refs
  field_path
  cause_execution_id
  suggested_action
 }
 class RecordResolver {
  resolve_authorized(ref)
  verify_digest_and_schema()
 }
 InvocationWrapper --> ModuleHandler : invokes
 InvocationWrapper --> RecordResolver : exact permitted inputs
 ModuleRequest --> RecordRef : inputs and pinned config
 ModuleResult --> RecordRef : outputs and diagnostics
 ModuleResult --> Diagnostic : explains disposition
 InvocationWrapper --> ModuleRequest : validates
 InvocationWrapper --> ModuleResult : publishes terminal result
```

Domain ownership remains distinct:

```mermaid
flowchart LR
 C[Capture] --> S[Surface]
 S --> M[Every fingerprint match]
 M --> L[SupportLink]
 L --> O[Coalesced collector Observation]
 O --> A[Canonical admission and verified binding]
 A --> F[Fact plus evidence and execution]
 F --> R[Complete ClaimResolution]
 R --> D[Derived or signal decision]
 D --> P[Grounded package]
 P --> G[Exact review and current-use gate]
 G --> X[Controlled export / separately allowed delivery]
```

Ordinary same-value duplicate matching adds support, not independent facts or probability. A failed producer, conflict, stale evidence or blocked gate must remain visible at the specific boundary rather than being summarized as an empty final package.
