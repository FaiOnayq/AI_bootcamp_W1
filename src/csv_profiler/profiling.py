
import json

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

    
def profile_rows(rows: list[dict[str, str]]) -> dict:
    n_rows = len(rows)
    columns_name = list(rows[0].keys())
    
    col_profiles = []
    for col in columns_name:
        values = [row.get(col, "") for row in rows]
        typ = infer_type(values)
        usable = [v for v in values if not is_missing(v)]
        missing = len(values) - len(usable)
        missing_pct = 100.0 * missing / n_rows if missing > 0 else 0.0
        unique = len(set(usable))
        profile = {
            "name": col,
            "type": typ,
            "missing": missing,
            "missing_pct": missing_pct,
            "unique": unique,
        }
        if typ == "number":
            nums =[]
            for i in usable:
                if try_float(i):
                    nums.append(float(i))
                else:
                    raise ValueError(f"Non-numeric value found: {i}")
            if nums:
                profile.update({"min": min(nums), "max": max(nums), "mean": sum(nums) / len(nums)})
        col_profiles.append(profile)

    
    
    return {"n_rows": n_rows, "n_cols": len(columns_name), "columns": col_profiles}