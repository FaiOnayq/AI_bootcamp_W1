from __future__ import annotations
from pathlib import Path
import json

from datetime import datetime

def md_header(source: str) -> list[str]:
    ts = datetime.now().isoformat(timespec="seconds")
    return [
        "# CSV Profiling Report",
        "",
        f"- **Source:** `{source}`",
        f"- **Generated:** `{ts}`",
        "",
    ]
    
def md_table_header() -> list[str]:
    return [
        "| Column | Type | Missing | Unique |",
        "|---|---:|---:|---:|",
    ]
    
def md_col_row(name: str, typ: str, missing: int, missing_pct: float, unique: int) -> str:
    return f"| `{name}` | {typ} | {missing} ({missing_pct:.1%}) | {unique} |"

def write_json(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def render_markdown(report: dict) -> str:
    lines: list[str] = []

    lines.append(f"# CSV Profiling Report\n")
    lines.append(f"Generated: {datetime.now().isoformat(timespec='seconds')}\n")

    lines.append("## Summary\n")
    lines.append(f"- Rows: **{report['n_rows']}**")
    lines.append(f"- Columns: **{report['n_cols']}**\n")

    lines.append("## Columns\n")
    lines.append("| name | type | missing | missing_pct | unique |")
    lines.append("|---|---:|---:|---:|---:|")
    lines.extend([
        f"| {c['name']} | {c['type']} | {c['missing']} | {c['missing_pct']:.1f}% | {c['unique']} |"
        for c in report["columns"]
    ])

    lines.append("\n## Notes\n")
    lines.append("- Missing values are: `''`, `na`, `n/a`, `null`, `none`, `nan` (case-insensitive)")

    return "\n".join(lines)