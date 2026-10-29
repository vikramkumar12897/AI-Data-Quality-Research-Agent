from pathlib import Path
import pandas as pd
OUT=Path(__file__).resolve().parent/"cases"; OUT.mkdir(exist_ok=True)
def w(name,rows): pd.DataFrame(rows).to_csv(OUT/f"{name}.csv",index=False)
def main():
 w("case_01_missing",[{"customer_id":"C1","country":"India","age":30,"activity_date":"2026-08-01"},{"customer_id":"C2","country":"India","age":None,"activity_date":"2026-08-02"},{"customer_id":"C3","country":"India","age":35,"activity_date":"2026-08-03"}])
 w("case_02_duplicates",[{"customer_id":"C1","country":"India","age":30},{"customer_id":"C1","country":"India","age":30},{"customer_id":"C2","country":"India","age":35}])
 w("case_03_category_aliases",[{"customer_id":"C1","country":"USA","age":30},{"customer_id":"C2","country":"US","age":31},{"customer_id":"C3","country":"U.S.","age":32},{"customer_id":"C4","country":"United States","age":33}])
 w("case_04_invalid_dates",[{"customer_id":"C1","country":"India","activity_date":"2026-08-01"},{"customer_id":"C2","country":"India","activity_date":"bad"},{"customer_id":"C3","country":"India","activity_date":"2026-08-03"}])
 w("case_05_outlier",[{"customer_id":"C1","age":25},{"customer_id":"C2","age":26},{"customer_id":"C3","age":27},{"customer_id":"C4","age":28},{"customer_id":"C5","age":500}])
 w("case_06_clean",[{"customer_id":"C1","country":"India","age":25},{"customer_id":"C2","country":"India","age":26},{"customer_id":"C3","country":"India","age":27},{"customer_id":"C4","country":"India","age":28}])
 w("case_07_mixed_issues",[{"customer_id":"C1","country":"USA","age":25,"activity_date":"2026-08-01"},{"customer_id":"C1","country":"US","age":25,"activity_date":"bad"},{"customer_id":"C2","country":"U.S.","age":26,"activity_date":"2026-08-03"},{"customer_id":"C3","country":"India","age":None,"activity_date":"2026-08-04"}])
 for i in range(8,13): w(f"case_{i:02d}_extra",[{"customer_id":f"C{i}1","country":"India","age":30+i},{"customer_id":f"C{i}2","country":"India","age":31+i},{"customer_id":f"C{i}3","country":"India","age":32+i}])
if __name__=="__main__": main()
