from __future__ import annotations
import json, os
import pandas as pd
import streamlit as st
from dotenv import load_dotenv
from app.core.profiler import profile_dataframe
from app.core.quality_checks import analyze_quality, quality_score
from app.reporting.report import build_markdown_report
load_dotenv()
st.set_page_config(page_title="AI Data Quality & Research Agent",page_icon="🔎",layout="wide")
st.title("🔎 AI Data Quality & Research Agent")
st.caption("Deterministic evidence → Research Agent → Verification Agent → Decision-ready report")
uploaded=st.file_uploader("Upload a CSV or XLSX dataset",type=["csv","xlsx"])
with st.sidebar:
 st.subheader("Workflow"); st.write("1. Profile"); st.write("2. Detect quality issues"); st.write("3. Research semantic/contextual findings"); st.write("4. Verify findings"); st.write("5. Generate report"); st.divider(); st.caption("API credentials stay local in .env and are never included in the submission ZIP.")
if uploaded:
 try:
  df=pd.read_csv(uploaded) if uploaded.name.lower().endswith('.csv') else pd.read_excel(uploaded)
 except Exception as exc:
  st.error(f"Could not read the file: {exc}"); st.stop()
 profile=profile_dataframe(df); findings=analyze_quality(df); score=quality_score(df,findings)
 c1,c2,c3,c4=st.columns(4); c1.metric("Rows",profile["rows"]); c2.metric("Columns",profile["columns"]); c3.metric("Duplicate rows",profile["duplicate_rows"]); c4.metric("Quality score",f"{score}/100")
 st.subheader("Dataset Profile"); st.dataframe(pd.DataFrame(profile["column_profiles"]),use_container_width=True)
 st.subheader("Deterministic Findings")
 if findings: st.dataframe(pd.DataFrame(findings)[["issue_id","category","severity","column","message","confidence"]],use_container_width=True)
 else: st.success("No issues were detected by the deterministic checks.")
 if st.button("Run Research + Verification Agents",type="primary",use_container_width=True):
  if not os.getenv("OPENAI_API_KEY"):
   st.warning("OPENAI_API_KEY is not available. Deterministic analysis works, but the agentic layer needs your local API key.")
  else:
   from app.agent_workflow.workflow import run_agentic_workflow
   with st.spinner("Running Research, Verification and Report agents..."):
    result=run_agentic_workflow(profile,findings)
   ar=result["report"].model_dump(); st.subheader("Agent Review"); st.write(ar["executive_summary"]); st.write(f"**Risk level:** {ar['risk_level']}")
   for rec in ar.get("recommendations",[]): st.write(f"• {rec}")
   if ar.get("research_notes"):
    st.subheader("Research Notes"); [st.write(f"• {n}") for n in ar["research_notes"]]
   md=build_markdown_report(profile,findings,score,ar)
   st.download_button("Download final report (Markdown)",data=md,file_name="data_quality_report.md",mime="text/markdown")
   st.download_button("Download findings (JSON)",data=json.dumps(findings,indent=2,default=str),file_name="findings.json",mime="application/json")
   st.success(f"Agent trajectory saved to: {result['trajectory_path']}")
else: st.info("Upload a dataset to begin. Try sample_data/demo_customers.csv.")
