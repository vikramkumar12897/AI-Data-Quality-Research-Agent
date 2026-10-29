import pandas as pd
from app.core.quality_checks import *

def test_missing(): assert check_missing_values(pd.DataFrame({"x":[1,None,3]}))[0]["category"]=="Completeness"
def test_duplicates(): assert check_duplicates(pd.DataFrame({"x":[1,1,2]}))[0]["category"]=="Uniqueness"
def test_aliases(): assert check_category_inconsistency(pd.DataFrame({"country":["USA","US","U.S."]}))[0]["category"]=="Consistency"
def test_invalid_dates(): assert check_date_validity(pd.DataFrame({"activity_date":["2026-01-01","bad"]}))[0]["category"]=="Validity"
def test_outlier(): assert check_numeric_outliers(pd.DataFrame({"age":[20,21,22,23,500]}))
def test_cross_column_conflict():
 future=(pd.Timestamp.today().normalize()+pd.Timedelta(days=10)).strftime("%Y-%m-%d"); df=pd.DataFrame({"status":["inactive"],"activity_date":[future]}); assert check_cross_column_conflicts(df)[0]["category"]=="Cross-column consistency"
def test_analyze_quality_combines():
 df=pd.DataFrame({"country":["USA","US"],"age":[20,None]}); assert len(analyze_quality(df))>=2
def test_score_decreases_with_findings():
 clean=pd.DataFrame({"x":[1,2,3,4]}); dirty=pd.DataFrame({"x":[1,None,3,1000]}); assert quality_score(dirty,analyze_quality(dirty))<=quality_score(clean,analyze_quality(clean))
