from Classes.Student import Student
from Classes.Exam import Exam

class Storage:
    def __init__(self):
        self.students = []
        self.exams = []

    def add_exam(self, id: int, exam_name: str, mark: int):
        self.exams.append(Exam(id, exam_name, mark))
        
    def add_student(self, id: int, fio: str, group_number: int):
        self.students.append(Student(id, fio, group_number))