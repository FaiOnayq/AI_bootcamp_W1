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
    
def write_markdown(report: dict, path: str | Path) -> None:
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)

    rows = report["summary"]["rows"]

    lines: list[str] = []
    lines.extend(md_header("data/sample.csv"))

    lines.append("## Summary")
    lines.append(f"- Rows: {rows:,}")
    lines.append(f"- Columns: {report['summary']['columns']:,}")
    lines.append("")

    lines.append("## Columns (table)")
    lines.extend(md_table_header())

    for name, col in report["columns"].items():
        missing_pct = (col["missing"] / rows) if rows else 0.0
        lines.append(md_col_row(name, col["type"], col["missing"], missing_pct, col["unique"]))

    lines.append("")
    lines.append("## Column details")

    for name, col in report["columns"].items():
        lines.append(f"### `{name}` ({col['type']})")

        if col["type"] == "number":
            lines.append(f"- min: {col['min']}")
            lines.append(f"- max: {col['max']}")
            lines.append(f"- mean: {col['mean']}")
        else:
            top = col.get("top", [])
            if not top:
                lines.append("- (no non-missing values)")
            else:
                lines.append("- top values:")
                for item in top:
                    lines.append(f"  - `{item['value']}`: {item['count']}")

        lines.append("")

    path.write_text("\n".join(lines) + "\n", encoding="utf-8")