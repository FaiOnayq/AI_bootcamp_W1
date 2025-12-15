from __future__ import annotations
from pathlib import Path
import json


def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    cols = report.get("columns", [])
    missing = report.get("missing", {})
    lines: list[str] = []
    lines.append("# CSV Profiling Report\n")
    lines.append(f"- Rows: **{report.get('rows', 0)}**")
    lines.append(f"- Columns: **{report.get('n_cols', 0)}**\n")

    lines.append("## Missing Values\n")
    lines.append("| column | missing |")
    lines.append("|---|---:|")
    for c in cols:
        lines.append(f"| {c} | {missing.get(c, 0)} |")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")