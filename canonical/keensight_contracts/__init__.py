"""KeenSight v4 design-time contracts and pure validation helpers.

No live collectors, database runtime, or sending integrations are implemented.
"""
__version__ = "4.2.0"

from . import ledger_catalog as _ledger_catalog  # Register all exported value shapes.
