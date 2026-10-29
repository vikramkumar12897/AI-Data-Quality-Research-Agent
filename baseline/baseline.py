from __future__ import annotations
import json,sys
from pathlib import Path
import pandas as pd
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT))
from app.core.quality_checks import check_missing_values, check_duplicates
def baseline_report(df): return {"rows":len(df),"columns":len(df.columns),"findings":check_missing_values(df)+check_duplicates(df)}
if __name__=="__main__":
 path=Path(sys.argv[1] if len(sys.argv)>1 else "sample_data/demo_customers.csv"); print(json.dumps(baseline_report(pd.read_csv(path)),indent=2,default=str))
