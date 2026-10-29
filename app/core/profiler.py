from __future__ import annotations
from typing import Any
import pandas as pd

def profile_dataframe(df: pd.DataFrame) -> dict[str, Any]:
    rows, cols = df.shape
    profiles=[]
    for col in df.columns:
        s=df[col]; non_null=int(s.notna().sum()); missing=int(s.isna().sum()); unique=int(s.nunique(dropna=True))
        p={"column":str(col),"dtype":str(s.dtype),"missing_count":missing,"missing_pct":round(missing/rows*100,2) if rows else 0.0,"unique_count":unique,"unique_pct":round(unique/non_null*100,2) if non_null else 0.0}
        if pd.api.types.is_numeric_dtype(s):
            clean=pd.to_numeric(s,errors="coerce").dropna()
            if not clean.empty:
                p.update({"min":float(clean.min()),"max":float(clean.max()),"mean":float(clean.mean()),"median":float(clean.median()),"std":float(clean.std(ddof=0))})
        profiles.append(p)
    return {"rows":int(rows),"columns":int(cols),"duplicate_rows":int(df.duplicated().sum()),"column_profiles":profiles}
