

    
    
MISSING = {"", "na", "n/a", "null", "none", "nan"}

def is_missing(value: str | None) -> bool:
    """True for empty / null-ish CSV values."""
    if value is None:
        return True
    
    return (value.strip().casefold()) in MISSING 

def try_float(value: str) -> float | None:
    try:
        return float(value)
    except ValueError:
        return None

def infer_type(values: list[str]) -> str:
    usable = [v for v in values if not is_missing(v)]
    if not usable:
        return "text"
    for v in usable:
        if try_float(v) is None:
            return "text"
    return "number"

def column_values(rows: list[dict[str, str]], col: str) -> list[str]:
    values = [row.get(col, "") for row in rows]
    return values

def numeric_stats(values: list[str]) -> dict:
    """Compute stats for numeric column values (strings)."""
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    nums =[]
    for i in usable:
        if try_float(i):
            nums.append(float(i))
        else:
            raise ValueError(f"Non-numeric value found: {i}")

    count = len(nums)
    unique = len(set(nums))
    return {
        "count": count,
        "missing": missing,
        "unique": unique,
        "min": min(nums) ,
        "max": max(nums),
        "mean": sum(nums)/count 
    }
    
    
def text_stats(values: list[str], top_k: int = 5) -> dict:
    usable = [v for v in values if not is_missing(v)]
    missing = len(values) - len(usable)
    
    counts = {}
    for v in usable:
        counts[v] = counts.get(v, 0) + 1
        
    top_items = sorted(counts.items(), key=lambda kv: kv[1], reverse=True)[:top_k]
    top = [{"value": v, "count": c} for v, c in top_items]
    
    return {
        "count": len(usable),
        "missing": missing,
        "unique": len(counts),
        "top": top,
    }
    


def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Compute row count, column names, and missing values per column."""
    rows_count = len(rows)

    cols = list(rows[0].keys())
    
    report = {
        "summary": {
            "rows": len(rows),
            "columns": len(cols),
            "column_names": cols,
        },
        "columns": {},
    }

    for col in cols:
        values = column_values(rows, col)
        typ = infer_type(values)

        if typ == "number":
            stats = numeric_stats(values)
        else:
            stats = text_stats(values)

        report["columns"][col] = {"type": typ, **stats}

    return report

rows = [{'name': 'Aisha', 'age': '23', 'city': 'Riyadh', 'salary': '12000'},
{'name': 'Fahad', 'age': '', 'city': 'Jeddah', 'salary': '9000'},
{'name': 'Noor', 'age': '29', 'city': '', 'salary': ''}]
basic_profile(rows)