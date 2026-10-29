import pandas as pd
from app.core.profiler import profile_dataframe

def test_profile_shape_and_duplicates():
 df=pd.DataFrame({"id":[1,1,2],"value":[10,20,30]}); r=profile_dataframe(df); assert r["rows"]==3 and r["columns"]==2 and r["duplicate_rows"]==0

def test_profile_missing_pct():
 df=pd.DataFrame({"id":[1,None,3]}); r=profile_dataframe(df); assert r["column_profiles"][0]["missing_count"]==1 and r["column_profiles"][0]["missing_pct"]==33.33
