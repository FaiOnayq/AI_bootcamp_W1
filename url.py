import csv
from io import StringIO
import httpx
import streamlit as st


use_url = st.sidebar.checkbox("Load from URL", value=False)

url = ""
if use_url:
    url = st.sidebar.text_input("CSV URL", placeholder="https://.../data.csv")

if use_url:
    if url == "":
        st.warning("Paste a URL to load a CSV.")
        st.stop()

    try:
        r = httpx.get(url, timeout=10.0)
        r.raise_for_status()
        text = r.text
        rows = list(csv.DictReader(StringIO(text)))
    except Exception as e:
        st.error("Failed to load URL: " + str(e))
        st.stop()