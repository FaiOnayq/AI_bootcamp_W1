def slugify(text: str) -> str:
    """Turn 'Report Name' → 'report-name'."""
    return text.casefold().string().replace(" ","-")