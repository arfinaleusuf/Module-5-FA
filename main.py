from fastapi import FastAPI, Path, HTTPException, Query, Body
from pydantic import BaseModel, Field
from typing import Annotated
import json

app = FastAPI()

class Student(BaseModel):
    id : Annotated[str,Field(...,description="Student id of the student", example="S001")]
    name : str
    age : Annotated[int, Field(...,gt=0, lt=100 ,description="Student age of the student", example="12")]
    Student_class : Annotated[int, Field(...,gt=0, lt=13)]
    roll: Annotated[int, Field(...,gt=0, lt=101)]
    Math_marks: Annotated[int, Field(...,gt=0, lt=101)]
    English_marks: Annotated[int, Field(...,gt=0, lt=101)]
    Science_marks: Annotated[int, Field(...,gt=0, lt=101)]
    Phone: Annotated[int, Field(...,examples="01700000000")]

@app.get("/")
def hello():
    return "Student Management System API"

def load_data():
    with open('student.json','r') as f:
        data = json.load(f)
    return data

def save_data(data):
    with open('student.json','w') as f:
        json.dump(data, f)

@app.get("/about")
def about():
    return "a fully functional API to manage our student records"

@app.get("/view")
def view_students():
    data = load_data()
    return data

@app.get("/view/{student_id}")
def view_students_by_id(student_id: str = Path(...,description="Student id of the student", example="S001")):
    data = load_data()

    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code=404, detail='student not found')
    

@app.get("/sort")
def view_sorted_students(sorted_by: str = Query(...,description="sort on the basis of Student_class, age, roll, marks", example=""), order: str = Query('asc', description='choose order: asc or desc')):
    valid_fields = ["age", "Student_class", "roll", "Math marks", "English marks", "Science marks",]

    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f'Invalid fields, select from{valid_fields}')

    if order not in ['asc','desc']:
        raise HTTPException(status_code=404, detail='choose between asc or desc')

    data = load_data()

    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by])
        return sorted_data
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key= lambda x: x[sorted_by], reverse=True)
        return sorted_data

@app.post("/create")
def create_student(student: Student):

    data = load_data()
    student_id = student["id"]

    data[student_id] = student
    del data[student_id]["id"]

    save_data(data)

    return "Successfully student created"
