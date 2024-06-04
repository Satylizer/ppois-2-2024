class Student:
    def __init__(self, id: int, fio: str, group_number: int):
        self.fio = fio
        self.group_number = group_number
        self.stud_id = id
        
    def __str__(self):
        return f"ID: {self.stud_id}, FIO: {self.fio}, Group: {self.group_number}"