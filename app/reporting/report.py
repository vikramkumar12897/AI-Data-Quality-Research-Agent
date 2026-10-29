from __future__ import annotations
def build_markdown_report(profile,findings,score,agent_report=None):
 critical=[f for f in findings if f["severity"]=="critical"]; warnings=[f for f in findings if f["severity"]=="warning"]
 lines=["# AI Data Quality & Research Report","",f"**Quality score:** {score}/100",f"**Rows:** {profile['rows']}",f"**Columns:** {profile['columns']}",f"**Duplicate rows:** {profile['duplicate_rows']}","","## Issue Summary","",f"- Critical issues: {len(critical)}",f"- Warnings: {len(warnings)}",f"- Total findings: {len(findings)}","","## Findings",""]
 for i,f in enumerate(findings,1):
  lines += [f"### {i}. {f['message']}",f"- **Category:** {f['category']}",f"- **Severity:** {f['severity']}",f"- **Confidence:** {f['confidence']:.0%}",f"- **Column:** {f['column'] or 'Dataset-wide'}",f"- **Evidence:** `{f['evidence']}`",f"- **Recommendation:** {f['recommendation']}",""]
 if agent_report:
  lines += ["## Agent Review","",f"**Risk level:** {agent_report.get('risk_level','N/A')}","",agent_report.get('executive_summary',''),"","### Recommendations",""]
  lines += [f"- {r}" for r in agent_report.get('recommendations',[])] + [""]
  if agent_report.get('research_notes'):
   lines += ["### Research Notes",""]+[f"- {n}" for n in agent_report['research_notes']]+[""]
 return "\n".join(lines)
