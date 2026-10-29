from __future__ import annotations
from typing import Any
import numpy as np
import pandas as pd

CATEGORY_ALIASES={
 "usa":{"usa","us","u.s.","u.s.a","united states","united states of america"},
 "uk":{"uk","u.k.","united kingdom","great britain","gb"},
 "india":{"india","in","bharat"},
}

def _issue(issue_id,category,column,severity,message,evidence,recommendation,confidence=0.95):
 return {"issue_id":issue_id,"category":category,"column":column,"severity":severity,"message":message,"evidence":evidence,"recommendation":recommendation,"confidence":confidence}

def check_missing_values(df):
 out=[]
 for col in df.columns:
  count=int(df[col].isna().sum())
  if count:
   pct=count/len(df)*100 if len(df) else 0
   out.append(_issue(f"missing::{col}","Completeness",str(col),"critical" if pct>=20 else "warning",f"{count} missing values ({pct:.1f}%) found.",{"missing_count":count,"missing_pct":round(pct,2)},"Fill, remove, or explicitly model missing values before analysis."))
 return out

def check_duplicates(df):
 count=int(df.duplicated().sum())
 if not count: return []
 pct=count/len(df)*100 if len(df) else 0
 return [_issue("duplicates::rows","Uniqueness",None,"critical" if pct>=5 else "warning",f"{count} duplicate rows ({pct:.1f}%) detected.",{"duplicate_rows":count,"duplicate_pct":round(pct,2)},"Deduplicate or define a business rule for legitimate repeated records.")]

def check_numeric_outliers(df):
 out=[]
 for col in df.select_dtypes(include=np.number).columns:
  s=df[col].dropna()
  if len(s)<5: continue
  q1,q3=s.quantile([0.25,0.75]); iqr=q3-q1
  if iqr==0: continue
  lower,upper=q1-1.5*iqr,q3+1.5*iqr; mask=(df[col]<lower)|(df[col]>upper); count=int(mask.sum())
  if count:
   out.append(_issue(f"outlier::{col}","Anomaly",str(col),"warning",f"{count} statistically unusual values detected using the IQR rule.",{"count":count,"pct":round(count/len(df)*100,2),"lower_bound":float(lower),"upper_bound":float(upper)},"Review flagged values against the business context before removing them.",0.90))
 return out

def check_date_validity(df):
 out=[]
 for col in df.columns:
  name=str(col).lower()
  if "date" not in name and "time" not in name: continue
  parsed=pd.to_datetime(df[col],errors="coerce"); mask=df[col].notna() & parsed.isna(); count=int(mask.sum())
  if count:
   out.append(_issue(f"invalid_date::{col}","Validity",str(col),"critical",f"{count} non-empty values could not be parsed as dates.",{"invalid_count":count},"Standardize date format and validate the source values."))
 return out

def check_category_inconsistency(df):
 out=[]
 for col in df.columns:
  s=df[col].dropna()
  if s.empty or not pd.api.types.is_object_dtype(s): continue
  values=[str(v).strip() for v in s.unique()]
  for canon,aliases in CATEGORY_ALIASES.items():
   present=[v for v in values if v.casefold() in aliases]
   if len({v.casefold() for v in present})>=2:
    out.append(_issue(f"category_alias::{col}::{canon}","Consistency",str(col),"warning",f"Multiple labels appear to represent the same category: {sorted(set(present))}.",{"canonical_candidate":canon,"variants":sorted(set(present))},"Normalize category labels using a governed mapping before aggregation.",0.80))
 return out

def check_cross_column_conflicts(df):
 out=[]; lower={str(c).lower():c for c in df.columns}
 status=next((lower[k] for k in lower if "status" in k),None); date=next((lower[k] for k in lower if "activity" in k and "date" in k),None)
 if status is not None and date is not None:
  future=(df[status].astype(str).str.casefold().isin({"inactive","closed","cancelled"}) & pd.to_datetime(df[date],errors="coerce").gt(pd.Timestamp.today().normalize()))
  count=int(future.sum())
  if count:
   out.append(_issue("cross_column::status_activity_date","Cross-column consistency",str(status),"warning",f"{count} rows have an inactive-like status but a future activity date.",{"conflicting_rows":count,"related_column":str(date)},"Confirm the business rule or correct the conflicting fields.",0.85))
 return out

def analyze_quality(df):
 findings=[]
 for fn in [check_missing_values,check_duplicates,check_numeric_outliers,check_date_validity,check_category_inconsistency,check_cross_column_conflicts]:
  findings.extend(fn(df))
 return findings

def quality_score(df,findings):
 if len(df)==0:return 0.0
 penalty=sum({"critical":12,"warning":5,"info":1}.get(f["severity"],1) for f in findings)
 return round(max(0.0,min(100.0,100.0-penalty)),1)
