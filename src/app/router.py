from fastapi import APIRouter, Depends
from src.app.schema import FilterSchema
from src.app import controller as control
import math

router = APIRouter()


async def paginate_dataframe(data, page_number, page_size):
    start_index = (page_number - 1) * page_size
    end_index = start_index + page_size
    return data.iloc[start_index:end_index]


@router.get("/employee")
async def app_router(
    filter: FilterSchema = Depends(),
    # per_page: int = Query(default=30),
    # skip: int = Query(default=0),
    # page_number: int = Query(default=1),
):
    paginate = True
    data = await control.get_employee_record()
    data = data.fillna("")
    data["Gender"] = [
        "F" if value == 0 else "M" if value == 1 else "F" for value in data["Gender"]
    ]

    data = data[(data["Emp_Left"] == "N")]

    if filter.gender:
        data = data[(data["Gender"] == f"{filter.gender}")]
    if filter.dept_name:
        data = data[(data["Dept_Name"] == f"{filter.dept_name}")]
    if filter.state:
        data = data[(data["State"] == f"{filter.state}")]
    if filter.city:
        data = data[(data["City"] == f"{filter.city}")]
    if filter.dob:
        data = data[(data["Date_Of_Birth"] == f"{filter.dob}")]
    if filter.basic_salary:
        data = data[(data["Basic_Salary"] == filter.basic_salary)]
    if filter.gross_salary:
        data = data[(data["Gross_Salary"] == filter.gross_salary)]
    if filter.atrrition:
        data = data[(data["Atrrition"] == filter.atrrition)]

    total_female = data[(data["Gender"] == "F")]
    total_male = data[(data["Gender"] == "M")]
    total_yes = data[(data["Atrrition"] == "Yes")]
    total_no = data[(data["Atrrition"] == "No")]

    # Unique Dept Data

    dept_values = data["Dept_Name"].value_counts(dropna=False).keys().tolist()
    dept_counts = data["Dept_Name"].value_counts(dropna=False).tolist()
    # dept_dict = dict(zip(values, counts))

    left_list = data["Emp_Left"].unique()
    unique_emp_left_list = left_list.tolist()

    # Unique State Data
    state_key_list = data["State"].unique()
    state_value_list = data["State"].value_counts()
    unique_state_key_list = state_key_list.tolist()
    unique_state_value_list = state_value_list.tolist()

    # City Column Work
    data['City'].replace('', 'Unknown', inplace=True)

    # Day Cal Culated
    day_key_list = data["Predicted_Day"].unique()
    srt_key = sorted(day_key_list)
    day_value_list = data["Predicted_Day"].value_counts()[srt_key].tolist()

    # Empt Attrition Count
    atrrition_values = data["Atrrition"].value_counts().keys().tolist()
    atrrition_counts = data["Atrrition"].value_counts().tolist()

    if paginate:
        total_result = len(data["Emp_ID"])
    #     total_page = math.ceil(total_result / per_page)
    #     data = await paginate_dataframe(
    #         data, page_number=page_number, page_size=per_page
    #     )

    res = data.to_dict(orient="records")

    result = {
        "emp_list": res,
        "dept_list": {
            "key": dept_values,
            "value_count": dept_counts,
            "label": "Department Wise Emp count",
        },
        "unique_emp_left": unique_emp_left_list,
        "state_list": {
            "key": unique_state_key_list,
            "value_count": unique_state_value_list,
        },
        "day_list": {"key": srt_key, "value_count": day_value_list},
        "atrrition_data": {
            "key": atrrition_values,
            "value_count": atrrition_counts,
            "label": "Atrrition Count",
        },
        "total_male": len(total_male),
        "total_female": len(total_female),
        "total_pred_yes": len(total_yes),
        "total_pred_no": len(total_no),
        "total_dept": len(dept_values),
        "total": total_result,
    }

    return result
