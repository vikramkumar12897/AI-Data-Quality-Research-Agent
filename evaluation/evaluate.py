from __future__ import annotations
import json
from pathlib import Path
import pandas as pd
from app.core.quality_checks import analyze_quality
ROOT=Path(__file__).resolve().parents[1]; CASES=ROOT/"evaluation/cases"; OUT=ROOT/"reports/evaluation_results.json"
GROUND={"case_01_missing.csv":{"Completeness"},"case_02_duplicates.csv":{"Uniqueness"},"case_03_category_aliases.csv":{"Consistency"},"case_04_invalid_dates.csv":{"Validity"},"case_05_outlier.csv":{"Anomaly"},"case_06_clean.csv":set(),"case_07_mixed_issues.csv":{"Uniqueness","Consistency","Completeness","Validity"},"case_08_extra.csv":set(),"case_09_extra.csv":set(),"case_10_extra.csv":set(),"case_11_extra.csv":set(),"case_12_extra.csv":set()}
def metrics(pred,gold):
 tp=len(pred&gold); fp=len(pred-gold); fn=len(gold-pred); p=tp/(tp+fp) if tp+fp else 1.0; r=tp/(tp+fn) if tp+fn else 1.0; f=2*p*r/(p+r) if p+r else 0.0; return {"precision":round(p,4),"recall":round(r,4),"f1":round(f,4)}
def main():
 rows=[]
 for path in sorted(CASES.glob("*.csv")):
  pred={f["category"] for f in analyze_quality(pd.read_csv(path))}; gold=GROUND.get(path.name,set()); rows.append({"case":path.name,"predicted_families":sorted(pred),"gold_families":sorted(gold),**metrics(pred,gold)})
 OUT.parent.mkdir(exist_ok=True); OUT.write_text(json.dumps(rows,indent=2),encoding="utf-8"); print(json.dumps(rows,indent=2))
if __name__=="__main__": main()
