from Classes.Model import Model
from Classes.Storage import Storage

class Controller:
    def __init__(self, storage: Storage):
        self.model = Model(storage)
        
    def add_student(self, id: int, fio: str, group_number: int):
        return self.model.add_student(id, fio, group_number)
    
    def add_exam(self, student_id: int, exam_name: str, mark: int):  # Use student_id
        return self.model.add_exam(student_id, exam_name, mark)

    def get_all_students(self):
        return self.model.get_all_students()
    
    def get_all_exams(self):
        return self.model.get_all_exams()
    
    def get_student_by_id(self, id):
        return self.model.get_student_by_id(id)
    
    def search_by_average_mark(self, min_mark, max_mark):
        return self.model.search_by_average_mark(min_mark, max_mark)

    def search_by_group_number(self, group_number):
        return self.model.search_by_group_number(group_number)

    def search_by_mark(self, mark):
        return self.model.search_by_mark(mark)

    def search_by_subject(self, subject):
        return self.model.search_by_subject(subject)
    
    def delete_by_average_mark(self, found_students, found_exams):
        return self.model.delete_by_average_mark(found_students, found_exams)

    def delete_by_group_number(self, found_students, found_exams):
        return self.model.delete_by_group_number(found_students, found_exams)

    def delete_by_mark(self, found_students, found_exams):
        return self.model.delete_by_mark(found_students, found_exams)

    def delete_by_subject(self, found_students, found_exams):
        return self.model.delete_by_subject(found_students,found_exams)
    
