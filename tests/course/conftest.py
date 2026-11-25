import sys
from pathlib import Path

# корень репо в sys.path, чтобы pytest работал и без python -m
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
