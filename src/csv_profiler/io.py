from __future__ import annotations
from csv import DictReader
from pathlib import Path

def read_csv_rows(path: str | Path) -> list[dict[str, str]]:
    """Read a CSV as a list of rows (each row is a dict of strings)."""
    path = Path(path)
    if not path.exists():
        raise FileNotFoundError(f"CSV not found: {path}")
    
    with open(path, "r", encoding="utf-8" ,newline="") as f:
        reader = DictReader(f)
        rows = [dict(row) for row in reader]
        if not rows:
            raise ValueError("The CSV has no data")
        return rows
    
