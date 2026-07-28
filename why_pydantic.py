def insert_student(name: str, math : int, eng: int):

    if type(math) == int and type(eng) == int:
        total = math + eng
        print(total)
    else:
        print("Worng data type")

insert_student('sakib',34,78)