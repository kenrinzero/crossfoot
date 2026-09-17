"""Local helper. The tracked corpus gate is `uv run python reconcile.py --all`."""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(root))

from reconcile import sweep

if __name__ == "__main__":
    raise SystemExit(sweep(root))
