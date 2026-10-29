import pandas as pd
from baseline.baseline import baseline_report

def test_baseline_contains_basic_checks():
 r=baseline_report(pd.DataFrame({"id":[1,1],"name":["A","A"]})); cats={f["category"] for f in r["findings"]}; assert "Completeness" not in cats and "Uniqueness" in cats

def test_baseline_detects_missing():
 r=baseline_report(pd.DataFrame({"id":[1,2],"name":[None,"A"]})); cats={f["category"] for f in r["findings"]}; assert "Completeness" in cats
