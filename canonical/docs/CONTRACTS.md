# Contract semantics

The authoritative v4.1 completion rules are [SYSTEM.md](../SYSTEM.md). Every new or changed field is enumerated in [CLASS_REFERENCE.md](CLASS_REFERENCE.md), generated from the schemas.

The generic Fact envelope is not sufficient validation: dispatch to the registered target/value shapes, then validate references, producer success, input closure, claim resolution, evidence, scope, authority and consuming-purpose eligibility. Do not treat schema validity as source truth.

Review and gate records have different jobs. Historical approval is not permission for a current external action. Current gates fail closed when input rights or evidence change. Stored immutable records must be resolved through trusted tenant/authentication context in the production repository. The legacy ChangeRecord authorization gap remains explicitly out of scope.
