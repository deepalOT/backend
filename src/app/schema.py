from pydantic import Field, BaseModel
from datetime import datetime
from typing import Optional
# E.Gender, E.Date_Of_Birth, E.Date_Of_Join, E.Emp_Left_Date, E.State, E.City, E.Probation, E.Emp_Notice_Period, S.Basic_Salary, S.Gross_Salary

class EmployeeBaseSchema(BaseModel):
    Emp_Left : Optional[str] = Field(default=None)
    Alpha_Emp_Code: Optional[str] = Field(default=None)
    Gender: Optional[str] = Field(default=None)
    Date_Of_Birth: Optional[datetime] = Field(default=None)
    Date_Of_Join: Optional[datetime] = Field(default=None)
    Emp_Left_Date: Optional[datetime] = Field(default=None)
    State: Optional[str] = Field(default=None)
    City: Optional[str] = Field(default=None)
    Probation: Optional[float] = Field(default=None)
    Basic_Salary: Optional[float] = Field(default= None)
    Gross_Salary: Optional[float] = Field(default= None)


    class Config():
        from_attributes=True

class FilterSchema(BaseModel):
    gross_salary: Optional[float] = Field(default=None)
    basic_salary: Optional[float] = Field(default=None)
    dept_name : Optional[str] = Field(default=None)
    probation: Optional[int] = Field(default=None)
    atrrition: Optional[str] = Field(default=None)
    emp_left : Optional[str] = Field(default=None)
    gender : Optional[str] = Field(default=None)
    state : Optional[str] = Field(default=None)
    city : Optional[str] = Field(default=None)
    dob: Optional[str] = Field(default=None)
    np: Optional[int] = Field(default=None)

