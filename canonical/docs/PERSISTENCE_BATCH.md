# Persistence and current-use boundaries

This revision implements reference guards and a local fixture JSON export, not a transactional database runtime. Keep one application, one database and a sequential runner.

Persist immutable observations and exact input references. Executions and per-target completion must commit consistently; related outputs must not become eligible before the producer succeeds. Replay/import records are distinct from live captures. A failed or unbound capture can stop at the AcquisitionAttempt diagnostic.

For current use, recheck the relevant state version at the side-effect boundary. The reference uses a conservative whole-bundle vector. A real multi-process exporter needs transactional serialization or compare-and-swap against authoritative state; a reference check followed by an external API call is not an atomic distributed transaction.

LocalPreviewExporter supports only DESIGN_TEST local files. It uses exclusive creation, byte verification on retry and fsync. Interrupted partial files are rejected rather than overwritten. Remote idempotency, reconciliation, crash recovery and an outbox remain runtime requirements, not completed features. UNKNOWN export state cannot be treated as a confirmed receipt. Sending stays disabled.
