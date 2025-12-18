import streamlit as st
from csv_profiler.io import read_csv_rows
from csv_profiler.profiling import profile_rows
from csv_profiler.render import render_markdown
from pathlib import Path
import json
import csv
from io import StringIO

st.set_page_config(page_title="CSV Profiler", layout="wide")
st.title("CSV Profiler")

st.sidebar.header("Inputs")
source = st.sidebar.selectbox("Data source", ["Upload"])
st.write("Selected:", source)

st.caption("Upload CSV file to build the profile JSON and MarkDown")


uploaded = st.file_uploader("Upload a CSV", type=["csv"])
if uploaded is not None:
    st.write("Filename:", uploaded.name)
    
    text = uploaded.getvalue().decode("utf-8-sig")
    file_like = StringIO(text)
    reader = csv.DictReader(file_like)   
    rows = list(reader)                  
    show_preview = st.checkbox("Show preview", value=True)

    if show_preview == True:
        st.subheader("Preview")
        st.write(rows[:5])  
        
    cols = st.columns(2)
    cols[0].metric("Rows", len(rows))
    if len(rows)==0:
        st.error("CSV loaded but has no data rows.")
        st.stop()
    if len(rows[0])==0:
        st.warning("The CSV file has no columns")
    cols[1].metric("Columns", len(rows[0]) if len(rows)>0 else 0 )
    
    if rows is not None and len(rows)>0:
        if st.button("Generate report"):
            st.session_state["report"] = profile_rows(rows)
        
else:
    st.info("Upload a CSV to begin.")

report = st.session_state.get("report")
if report is not None:
    st.write("Top missing Columns: ")

    top_key = 3
    top3 = sorted( report.get("columns"), key=lambda x: x.get("missing_pct", 0), reverse=True)[:top_key]
    nameTop = [name.get("name") for name in top3]
    
    for x in range(top_key):
        st.write(f"{x+1}. {nameTop[x]}")
    
    st.subheader("Markdown preview")
    st.markdown(render_markdown(report))
    #st.write(render_markdown(report))
    
    st.title("Download and Save")
    name = st.text_input("Report Name:", placeholder="report")
    
    if name is None or name=="":
        name = "report"
        
    
    st.subheader("Download:")
    cols_download = st.columns(2)
    cols_download[0].download_button("Download JSON", data=json.dumps(report, indent=2, ensure_ascii=False), file_name = name+".json")
    cols_download[1].download_button("Download Markdown", data=render_markdown(report), file_name= (name+".md"))
    
    st.subheader("Save Locally:")
    cols = st.columns(2)
    out_dir = Path("outputs")
    out_dir.mkdir(parents=True, exist_ok=True)
    cols_local = st.columns(2)
    if cols_local[0].button("Download Json Locally"):
        (out_dir / (name+".json")).write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    if cols_local[1].button("Download MarkDown Locally"):
        (out_dir / (name+".md")).write_text(render_markdown(report), encoding="utf-8")

    
    
    

