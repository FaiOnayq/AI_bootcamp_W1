

def basic_profile(rows: list[dict[str, str]]) -> dict:
    """Compute row count, column names, and missing values per column."""
    rows_count = len(rows)

    column_names = list(rows[0].keys())
    
    missing = dict.fromkeys(column_names, 0)
    nonMissing = dict.fromkeys(column_names, 0)
    
    for row in rows:
        for col in column_names:
            if row.get(col)=='':
                missing[col]+=1
            else:
                nonMissing[col]+=1
    
    return {
        "rows": len(rows),
        "n_cols": len(column_names),
        "columns": column_names,
        "missing": missing,
        "non_empty": nonMissing,
    }