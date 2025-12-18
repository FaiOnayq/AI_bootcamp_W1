from pathlib import Path
import typer

import json
import time


from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown

app = typer.Typer()

@app.command(help="Profile a CSV file and write JSON + Markdown")
def profile(
    input_path: Path = typer.Argument(..., help="Input CSV file"),
    out_dir: Path = typer.Option(Path("outputs"), "--out-dir", help="Output folder"),
    report_name: str = typer.Option("report", "--report-name", help="Base name for outputs"),
    preview: bool = typer.Option(False, "--preview", help="Print a short summary"),
):
    # implementation comes in hands-on
    typer.echo(f"Input: {input_path}")
    typer.echo(f"Out:   {out_dir}")
    typer.echo(f"Name:  {report_name}")
    
    start = time.perf_counter_ns()
    
    rows = read_csv_rows(input_path)
    report = profile_rows(rows)
    
        
    
    out_dir.mkdir(parents=True, exist_ok=True)
    
    end = time.perf_counter_ns()
    elapsed_ms = (end - start) / 1_000_000
    report["elapsed_ms"] = elapsed_ms
    
    json_path = out_dir / f'{report_name}.json'
    json_path.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    
    md_path = out_dir / f'{report_name}.md'
    md = render_markdown(report)
    md_path.write_text(md, encoding="utf-8")
    
    
    if preview:
        typer.echo(f" CSV file Report \n Rows: {report['n_rows']} | Cols: {report['n_cols']} | time: {elapsed_ms}")



if __name__ == "__main__":
    app()
    