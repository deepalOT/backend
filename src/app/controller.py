import pickle
import numpy as np
import pandas as pd
from sqlalchemy.sql import text
from src.database.db_config import engine
from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import LabelEncoder
from datetime import datetime, date

sc = StandardScaler()
le = LabelEncoder()
today = date.today()


def age(born):
    if isinstance(born, str):
        born = datetime.strptime(born, "%Y/%m/%d").date()
        return (
            today.year - born.year - ((today.month, today.day) < (born.month, born.day))
        )
    else:
        return 0


async def get_record():
    sql_query = text(
        "Select E.Emp_ID, E.Alpha_Emp_Code, E.Emp_Left, E.Dept_ID, E.Gender, E.Date_Of_Birth, E.Date_Of_Join, E.Emp_Left_Date, E.State, E.City, E.Probation, S.Basic_Salary, S.Gross_Salary, D.Dept_Name from  T0080_EMP_MASTER E inner join T0200_MONTHLY_SALARY S on E.Emp_ID = S.Emp_ID inner join T0040_DEPARTMENT_MASTER D on E.Dept_ID = D.Dept_ID where E.Cmp_id in (119,120)"
    )
    data = pd.read_sql(sql_query, engine)

    data.drop_duplicates(subset=['Emp_ID'], inplace=True)  
    data = data[data['Dept_ID'].notna()]
    msk = (data['State'] == '<--SELECT-->')
    data = data[~msk]
    data['Gross_Salary'].fillna(data['Gross_Salary'].mean(), inplace=True)
    data = data[data['State'].notna()]
    data = data[data['City'].notna()]
    data = data.fillna('')
    
    data["Date_Of_Birth"] = data["Date_Of_Birth"].dt.strftime("%Y/%m/%d")
    data["Date_Of_Join"] = data["Date_Of_Join"].dt.strftime("%Y/%m/%d")

    return data


async def get_employee_record():
    with open("attr_model.pkl", "rb") as f:
        mod = pickle.load(f)

    result = await get_record()
    state_name = result['State']
    city_name = result['City']

    result['Gender'] = le.fit_transform(result['Gender'])
    result['State'] = le.fit_transform(result['State'])
    result['City'] = le.fit_transform(result['City'])

    result["Age"] = result["Date_Of_Birth"].apply(age)
    test_data_df = result[['Dept_ID','Age', 'Gender', 'State','City', 'Probation', 'Basic_Salary', 'Gross_Salary']]
    sc.fit(test_data_df)
    x_test = sc.transform(test_data_df) 
    pred = mod.predict(x_test)

    probabilities = mod.predict_proba(x_test)

    result['State'] = state_name
    result['City'] = city_name
    result["Atrrition"] = ["No" if value == 0 else "Yes" if value == 1 else "No" for value in pred.tolist()]
    result["Probabilities"] =  ["90 %" if value[0] >= 0.80 else "60 %" if value[0] >= 0.60 else "30 %" if value[0] >= 0.30 else "Stay" for value in probabilities.tolist()]
    result["Predicted_Day"] = ["30" if value[0] >= 0.80 else "90" if value[0] >= 0.60 else "60" if value[0] >= 0.30 else "0" for value in probabilities.tolist()]

    # Filter Dataframe

    return result
