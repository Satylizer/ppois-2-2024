from Classes.Storage import Storage
from Classes.removeDuplicates import remove_duplicate_students

class Model:  
    def __init__(self, storage: Storage):
        self.storage = storage
        
    def add_student(self, id: int, fio: str, group_number: int):
        return self.storage.add_student(id, fio, group_number)
    
    def add_exam(self, student_id: int, exam_name: str, mark: int):  # Use student_id
        return self.storage.add_exam(student_id, exam_name, mark)

    def get_all_students(self):
        return self.storage.students
    
    def get_all_exams(self):
        return self.storage.exams
    
    def get_student_by_id(self, id):
        for student in self.storage.students:
            if student.stud_id == id:
                return student
        return None

    def search_by_average_mark(self, min_mark, max_mark):
        found_students = []
        found_exams = []
        for exam in self.storage.exams:
            if exam.mark >= int(min_mark) and exam.mark <= int(max_mark):
                found_exams.append(exam)
        for student in self.storage.students:
            for exam in found_exams:
                if student.stud_id == exam.exam_id:
                        found_students.append(student)        
                        
        return {"found_students": remove_duplicate_students(found_students), "found_exams": found_exams}

    def search_by_group_number(self, group_number):
        found_students = []
        found_exams = []
        for student in self.storage.students:
            if student.group_number == int(group_number):
                found_students.append(student)
        found_students = remove_duplicate_students(found_students)
        for student in found_students:
            for exam in self.storage.exams:
                if student.stud_id == exam.exam_id:
                    found_exams.append(exam)
        return {"found_students": remove_duplicate_students(found_students), "found_exams": found_exams}

    def search_by_mark(self, mark):
        found_students = []
        found_exams = []
        for exam in self.storage.exams:
            if exam.mark == mark:
                found_exams.append(exam)
        for student in self.storage.students:
            for exam in found_exams:
                if student.stud_id == exam.exam_id:
                    found_students.append(student)
        return {"found_students": remove_duplicate_students(found_students), "found_exams": found_exams}

    def search_by_subject(self, subject):
        found_students = []
        found_exams = []
        for exam in self.storage.exams:
            if exam.name == subject:
                found_exams.append(exam)
        found_students = remove_duplicate_students(found_students)
        for student in self.storage.students:
            for exam in found_exams:
                if student.stud_id == exam.exam_id:
                    found_students.append(student)   
        return {"found_students": found_students, "found_exams": found_exams}
    
    def delete_by_average_mark(self, found_students, found_exams):
        deletion_count = 0
        for exam in found_exams:
            for ind, ex in enumerate(self.storage.exams):
                if exam.exam_id == ex.exam_id:
                    del self.storage.exams[ind]
                    deletion_count += 1
        return deletion_count

    def delete_by_group_number(self, found_students, found_exams):
        deletion_count = 0
        for student in found_students:
            self.storage.students.remove(student)
            deletion_count += 1
        for exam in found_exams:
            for ind, ex in enumerate(self.storage.exams):
                if exam.exam_id == ex.exam_id:
                    del self.storage.exams[ind]
                    deletion_count += 1
        return deletion_count

    def delete_by_mark(self, found_students, found_exams):
        deletion_count = 0
        for exam in found_exams:
            for ind, ex in enumerate(self.storage.exams):
                if exam.exam_id == ex.exam_id:
                    del self.storage.exams[ind]
                    deletion_count += 1
        return deletion_count

    def delete_by_subject(self, found_students, found_exams):
        deletion_count = 0
        for exam in found_exams:
            for ind, ex in enumerate(self.storage.exams):
                if exam.exam_id == ex.exam_id:
                    del self.storage.exams[ind]
                    deletion_count += 1
        return deletion_count