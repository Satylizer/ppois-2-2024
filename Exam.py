class Exam:
    def __init__(self, id: int, name: str, mark: int):
        self.name = name
        self.mark = mark
        self.exam_id = id
        
    def __str__(self):
        return f"ID: {self.exam_id}, Exam: {self.name}, Mark: {self.mark}"