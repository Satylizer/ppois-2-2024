import tkinter as tk
import xml.etree.ElementTree as ET
from tkinter import filedialog
from tkinter import messagebox
from tkinter import simpledialog
from Controller.controller import Controller
from Classes.Storage import Storage

class MyApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.storage = Storage()
        self.controller = Controller(self.storage)
        self.current_page = 1
        self.max_page = 10
        self.max_students_per_page = 10
        self.max_exams_per_page = 20
        

        self.title("Таблица студентов")
        self.configure(bg='#fafafa')
        self.attributes('-alpha', 0.9)
        self.geometry("1000x500")

        self.main_frame = tk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.top_frame = tk.Frame(self.main_frame, bg='#fafafa')
        self.top_frame.pack(side=tk.TOP, fill=tk.X)

        self.add_student_button = tk.Button(self.top_frame, text="Добавить студента", command=self.add_student)
        self.add_student_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.add_exam_button = tk.Button(self.top_frame, text="Добавить экзамен", command=self.add_exam)
        self.add_exam_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.search_button = tk.Button(self.top_frame, text="Поиск", command=self.search)
        self.search_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.delete_button = tk.Button(self.top_frame, text="Удаление", command=self.delete)
        self.delete_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.load_button = tk.Button(self.top_frame, text="Отображение", command=self.max_per_page)
        self.load_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.save_button = tk.Button(self.top_frame, text="Файловые операции", command=self.file_operations)
        self.save_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.top_frame2 = tk.Frame(self.main_frame, bg='#fafafa')
        self.top_frame2.pack(side=tk.TOP, fill=tk.X)

        self.label_student = tk.Label(self.top_frame2, text="ФИО студента", bg='#fafafa')
        self.label_student.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_group = tk.Label(self.top_frame2, text="Группа", bg='#fafafa')
        self.label_group.pack(side=tk.LEFT, padx=5, pady=5)

        self.label_exams = tk.Label(self.top_frame2, text="Экзамены", bg='#fafafa')
        self.label_exams.pack(side=tk.RIGHT, padx=5, pady=5)

        self.table_frame = tk.Frame(self.main_frame, bg='#fafafa')
        self.table_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        self.left_list = tk.Listbox(self.table_frame, width=20)
        self.left_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        self.right_list = tk.Listbox(self.table_frame, width=20)
        self.right_list.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        self.bottom_frame = tk.Frame(self.main_frame, bg='#fafafa')
        self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        self.prev_page_button = tk.Button(self.bottom_frame, text="Предыдущая страница", command=self.prev_page)
        self.prev_page_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.page_label = tk.Label(self.bottom_frame, text="Страница 1", bg='#fafafa')
        self.page_label.pack(side=tk.LEFT, padx=5, pady=5)

        self.next_page_button = tk.Button(self.bottom_frame, text="Следующая страница", command=self.next_page)
        self.next_page_button.pack(side=tk.LEFT, padx=5, pady=5)
        
        self.max_page_label = tk.Label(self.bottom_frame, text=f"Всего страниц:{self.max_page}")
        self.max_page_label.pack(side=tk.RIGHT, padx=5, pady=5)
        
    def file_operations(self):
        def save_data():
            filename = filedialog.asksaveasfilename(defaultextension=".xml", filetypes=[("XML files", "*.xml")])
            if filename:
                root = ET.Element("data")

                students_element = ET.SubElement(root, "students")
                for student in self.storage.students:
                    student_element = ET.SubElement(students_element, "student")
                    ET.SubElement(student_element, "stud_id").text = str(student.stud_id)
                    ET.SubElement(student_element, "name").text = student.fio
                    ET.SubElement(student_element, "group_number").text = str(student.group_number)

                exams_element = ET.SubElement(root, "exams")
                for exam in self.storage.exams:
                    exam_element = ET.SubElement(exams_element, "exam")
                    ET.SubElement(exam_element, "exam_id").text = str(exam.exam_id)
                    ET.SubElement(exam_element, "name").text = exam.name
                    ET.SubElement(exam_element, "mark").text = str(exam.mark)

                tree = ET.ElementTree(root)
                tree.write(filename, encoding='utf-8', xml_declaration=True)
                popup.destroy()

        def load_data():
            filename = filedialog.askopenfilename(filetypes=[("XML files", "*.xml")])
            if filename:
                try:
                    tree = ET.parse(filename)
                    root = tree.getroot()

                    self.storage.students = []
                    self.storage.exams = []

                    for student_element in root.find("students"):
                        stud_id = int(student_element.find("stud_id").text)
                        name = student_element.find("name").text
                        group_number = int(student_element.find("group_number").text)
                        self.storage.add_student(stud_id, name, group_number)

                    for exam_element in root.find("exams"):
                        exam_id = int(exam_element.find("exam_id").text)
                        name = exam_element.find("name").text
                        mark = int(exam_element.find("mark").text)
                        self.storage.add_exam(exam_id, name, mark)

                    self.update_exams_list()
                    self.update_students_list()
                    popup.destroy()

                except FileNotFoundError:
                    messagebox.showerror("Ошибка", "Файл не найден.")
                except ET.ParseError:
                    messagebox.showerror("Ошибка", "Неверный формат XML файла.")
                except Exception as e:
                    messagebox.showerror("Ошибка", f"Ошибка при загрузке данных: {e}")

        popup = tk.Toplevel(self.master)
        popup.title("Файловые операции")

        save_button = tk.Button(popup, text="Сохранить", command=save_data)
        save_button.pack(pady=5)

        load_button = tk.Button(popup, text="Загрузить", command=load_data)
        load_button.pack(pady=5)

        close_button = tk.Button(popup, text="Закрыть", command=popup.destroy)
        close_button.pack(pady=5)

    
    def max_per_page(self):
        popup = tk.Toplevel(self.master)
        popup.title("Отображение")

        def save_changes():
            new_students_per_page = students_entry.get()
            new_exams_per_page = exams_entry.get()
            
            if not new_students_per_page and not new_exams_per_page:
                popup.destroy()
                messagebox.showwarning("Предупреждение", "Хотя бы одно поле должно быть заполнено.")
                return

            try:
                if new_students_per_page:
                    self.max_students_per_page = int(new_students_per_page)
                    if not 0 <= self.max_students_per_page <= 20:
                        self.max_students_per_page = 10
                        messagebox.showwarning("Предупреждение","Значение для студентов должно быть от 0 до 20.")

                if new_exams_per_page:
                    self.max_exams_per_page = int(new_exams_per_page)
                    if not 0 <= self.max_exams_per_page <= 25:
                        self.max_exams_per_page = 20
                        messagebox.showwarning("Предупреждение","Значение для экзаменов должно быть от 0 до 25.")

                students_label.config(text=f"Студенты на странице: {self.max_students_per_page}")
                exams_label.config(text=f"Экзамены на странице: {self.max_exams_per_page}")

            except ValueError as e:
                popup.destroy()
                messagebox.showwarning("Ошибка", str(e))

        students_label = tk.Label(popup, text=f"Студенты на странице: {self.max_students_per_page}")
        students_label.pack(pady=5)
        exams_label = tk.Label(popup, text=f"Экзамены на странице: {self.max_exams_per_page}")
        exams_label.pack(pady=5)

        students_entry_label = tk.Label(popup, text="Студенты:")
        students_entry_label.pack(pady=2)
        students_entry = tk.Entry(popup)
        students_entry.pack(pady=2)

        exams_entry_label = tk.Label(popup, text="Экзамены:")
        exams_entry_label.pack(pady=2)
        exams_entry = tk.Entry(popup)
        exams_entry.pack(pady=2)

        save_button = tk.Button(popup, text="Сохранить", command=save_changes)
        save_button.pack(pady=5)



    def add_student(self):
        def save_student():
            fio = fio_entry.get()
            group_number = group_entry.get()
            if fio and group_number:
                if not group_number.isdigit():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "Номер группы должен быть целым числом")
                    return
                if not fio.isalpha():
                    add_student_window.destroy()
                    messagebox.showwarning("Ошибка", "ФИО студента должно содержать только буквы")
                    return
                student_id = len(self.storage.students) + 1
                self.controller.add_student(int(student_id), str(fio), int(group_number))
                self.update_students_list()
            else:
                add_student_window.destroy()
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")
                return

        add_student_window = tk.Toplevel(self.master)
        add_student_window.title("Добавить студента")

        fio_label = tk.Label(add_student_window, text="ФИО:")
        fio_label.grid(row=0, column=0, padx=5, pady=5)
        fio_entry = tk.Entry(add_student_window)
        fio_entry.grid(row=0, column=1, padx=5, pady=5)

        group_label = tk.Label(add_student_window, text="Группа:")
        group_label.grid(row=1, column=0, padx=5, pady=5)
        group_entry = tk.Entry(add_student_window)
        group_entry.grid(row=1, column=1, padx=5, pady=5)

        save_button = tk.Button(add_student_window, text="Сохранить", command=save_student)
        save_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)

    def add_exam(self):
        def save_exam():
            student_id = student_id_entry.get()
            exam_name = exam_name_entry.get()
            score = score_entry.get()   
            
            
            if exam_name and score and student_id:
                if not student_id.isdigit():
                            add_exam_window.destroy()
                            messagebox.showwarning("Ошибка", "Введите корректный ID студента (целое число)")
                            return
                
                existing_student = self.controller.get_student_by_id(int(student_id))
                if existing_student is None:
                    add_exam_window.destroy()
                    messagebox.showwarning("Ошибка", "Студент с указанным ID не существует")
                else:
                        if not exam_name.isalpha():
                            add_exam_window.destroy()
                            messagebox.showwarning("Ошибка", "Название экзамена должно содержать только буквы")
                            return
                        if not score.isdigit() or (int(score) < 0 or int(score) > 10):
                            add_exam_window.destroy()
                            messagebox.showwarning("Ошибка", "Оценка должна быть целым числом от 0 до 10")
                            return
                        self.controller.add_exam(int(student_id), str(exam_name), int(score))
                        self.update_exams_list()
            else:
                add_exam_window.destroy()
                messagebox.showwarning("Ошибка", "Пожалуйста, заполните все поля")


        add_exam_window = tk.Toplevel(self.master)
        add_exam_window.title("Добавить экзамен")

        student_id_label = tk.Label(add_exam_window, text="ID студента:")
        student_id_label.grid(row=0, column=0, padx=5, pady=5)
        student_id_entry = tk.Entry(add_exam_window)
        student_id_entry.grid(row=0, column=1, padx=5, pady=5)

        exam_name_label = tk.Label(add_exam_window, text="Название экзамена:")
        exam_name_label.grid(row=1, column=0, padx=5, pady=5)
        exam_name_entry = tk.Entry(add_exam_window)
        exam_name_entry.grid(row=1, column=1, padx=5, pady=5)

        score_label = tk.Label(add_exam_window, text="Оценка:")
        score_label.grid(row=2, column=0, padx=5, pady=5)
        score_entry = tk.Entry(add_exam_window)
        score_entry.grid(row=2, column=1, padx=5, pady=5)

        save_button = tk.Button(add_exam_window, text="Сохранить", command=save_exam)
        save_button.grid(row=3, column=0, columnspan=2, padx=5, pady=5)
            
    def update_students_list(self):
        self.left_list.delete(0, tk.END)

        students = self.controller.get_all_students()

        start_index = (self.current_page - 1) * self.max_students_per_page
        end_index = self.current_page * self.max_students_per_page

        for student in students[start_index:end_index]:
            self.left_list.insert(tk.END, student)

        self.page_label.config(text=f"Страница {self.current_page}")
            
    def update_exams_list(self):
        self.right_list.delete(0, tk.END)
        
        exams = self.controller.get_all_exams()
        
        start_index = (self.current_page - 1) * self.max_exams_per_page
        end_index = self.current_page * self.max_exams_per_page

        for exam in exams[start_index:end_index]:
            self.right_list.insert(tk.END, exam)


    def search(self):
        search_option = simpledialog.askinteger("Поиск", "Выберите опцию:\n1. По среднему баллу\n2. По номеру группы\n3. По баллу\n4. По предмету")
        if search_option == 1:
            self.search_by_average_mark(0)
        elif search_option == 2:
            self.search_by_group_number(0)
        elif search_option == 3:
            self.search_by_mark(0)
        elif search_option == 4:
            self.search_by_subject(0)
        else:
            messagebox.showwarning("Ошибка", "Неправильный ввод")

    def search_by_average_mark(self, select_num):
        def search_average_mark():
            min_mark = min_mark_entry.get()
            max_mark = max_mark_entry.get()
            
            if not min_mark.isdigit() or not max_mark.isdigit():
                search_average_mark_window.destroy()
                messagebox.showwarning("Ошибка", "Границы баллов должны быть целыми числами")
                return
            
            found_results = self.controller.search_by_average_mark(int(min_mark), int(max_mark))
            self.show_search_results(found_results["found_students"], found_results["found_exams"], select_num)
            search_average_mark_window.destroy()

        search_average_mark_window = tk.Toplevel(self.master)
        search_average_mark_window.title("Поиск по среднему баллу")

        min_mark_label = tk.Label(search_average_mark_window, text="Нижняя граница среднего балла:")
        min_mark_label.grid(row=0, column=0, padx=5, pady=5)
        min_mark_entry = tk.Entry(search_average_mark_window)
        min_mark_entry.grid(row=0, column=1, padx=5, pady=5)

        max_mark_label = tk.Label(search_average_mark_window, text="Верхняя граница среднего балла:")
        max_mark_label.grid(row=1, column=0, padx=5, pady=5)
        max_mark_entry = tk.Entry(search_average_mark_window)
        max_mark_entry.grid(row=1, column=1, padx=5, pady=5)

        search_button = tk.Button(search_average_mark_window, text="Поиск", command=search_average_mark)
        search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    def search_by_group_number(self, select_num):
        def search_group_number():
            group_number = group_entry.get()
            if not group_number.isdigit():
                search_group_number_window.destroy()
                messagebox.showwarning("Ошибка", "Номер группы должен быть целым числом")
                return
            found_results = self.controller.search_by_group_number(int(group_number))
            self.show_search_results(found_results["found_students"], found_results["found_exams"], select_num)
            search_group_number_window.destroy()

        search_group_number_window = tk.Toplevel(self.master)
        search_group_number_window.title("Поиск по номеру группы")

        group_label = tk.Label(search_group_number_window, text="Номер группы:")
        group_label.grid(row=0, column=0, padx=5, pady=5)
        group_entry = tk.Entry(search_group_number_window)
        group_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_group_number_window, text="Поиск", command=search_group_number)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def search_by_mark(self, select_num):
        def search_mark():
            mark = mark_entry.get()
            if not mark.isdigit():
                search_mark_window.destroy()
                messagebox.showwarning("Ошибка", "Количество баллов должно быть целым числом")
                return
            found_results = self.controller.search_by_mark(int(mark))
            self.show_search_results(found_results["found_students"], found_results["found_exams"], select_num)
            search_mark_window.destroy()

        search_mark_window = tk.Toplevel(self.master)
        search_mark_window.title("Поиск по баллу")

        mark_label = tk.Label(search_mark_window, text="Количество баллов:")
        mark_label.grid(row=0, column=0, padx=5, pady=5)
        mark_entry = tk.Entry(search_mark_window)
        mark_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_mark_window, text="Поиск", command=search_mark)
        search_button.grid(row=2, column=0, columnspan=2, padx=5, pady=5)


    def search_by_subject(self, select_num):
        def search_subject():
            subject = subject_entry.get()
            if not subject.isalpha():
                search_subject_window.destroy()
                messagebox.showwarning("Ошибка", "Название предмета должно содержать только буквы")
                return
            found_results = self.controller.search_by_subject(subject)
            self.show_search_results(found_results["found_students"], found_results["found_exams"], select_num)
            search_subject_window.destroy()

        search_subject_window = tk.Toplevel(self.master)
        search_subject_window.title("Поиск по предмету")

        subject_label = tk.Label(search_subject_window, text="Предмет:")
        subject_label.grid(row=0, column=0, padx=5, pady=5)
        subject_entry = tk.Entry(search_subject_window)
        subject_entry.grid(row=0, column=1, padx=5, pady=5)

        search_button = tk.Button(search_subject_window, text="Поиск", command=search_subject)
        search_button.grid(row=1, column=0, columnspan=2, padx=5, pady=5)


    def show_search_results(self, found_students, found_exams, select_num):
        if not found_students and not found_exams:
            messagebox.showinfSo("Поиск", "Ничего не найдено")
            return

        result_window = tk.Toplevel(self)
        result_window.title("Результаты поиска")
        result_window.geometry("500x500")

        top_frame = tk.Frame(result_window, bg='#fafafa')
        top_frame.pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        students_listbox = tk.Listbox(top_frame, width=20)
        students_listbox.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

        exams_listbox = tk.Listbox(top_frame, width=20)
        exams_listbox.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        bottom_frame = tk.Frame(result_window)
        bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)

        for student in found_students:
            student_info = f"ID: {student.stud_id}, ФИО: {student.fio}, Номер группы: {student.group_number}"
            students_listbox.insert(tk.END, student_info)

        for exam in found_exams:
            exam_info = f"ID: {exam.exam_id}, Название: {exam.name}, Балл: {exam.mark}"
            exams_listbox.insert(tk.END, exam_info)

        def confirm_delete(found_students, found_exams, select_num):
            confirm_delete_window = tk.Toplevel(result_window)
            confirm_delete_window.title("Подтверждение удаления")

            confirm_label = tk.Label(confirm_delete_window, text="Вы уверены, что хотите удалить выбранных студентов и экзамены?")
            confirm_label.pack(padx=10, pady=10)

            confirm_button = tk.Button(confirm_delete_window, text="Удалить", command=lambda: show_delete_confirmation(found_students, found_exams, select_num))
            confirm_button.pack(side=tk.LEFT, padx=10, pady=10)

            cancel_button = tk.Button(confirm_delete_window, text="Отмена", command=confirm_delete_window.destroy)
            cancel_button.pack(side=tk.RIGHT, padx=10, pady=10)

        def show_delete_confirmation(found_students, found_exams, select_num):
            deleted_count = confirm_delete_action(found_students, found_exams, select_num)
            messagebox.showinfo("Удаление", f"Удалено записей: {deleted_count}")


        def confirm_delete_action(found_students, found_exams, select_num):
            deleted_count = 0
            if select_num == 1:
                deleted_count = self.controller.delete_by_average_mark(found_students, found_exams)
            elif select_num == 2:
                deleted_count = self.controller.delete_by_group_number(found_students, found_exams)
            elif select_num == 3:
                deleted_count = self.controller.delete_by_mark(found_students, found_exams)
            elif select_num == 4:
                deleted_count = self.controller.delete_by_subject(found_students, found_exams)

            result_window.destroy()
            self.update_exams_list()
            self.update_students_list()
            return deleted_count


        if select_num in (1, 2, 3, 4):
            delete_button = tk.Button(bottom_frame, text="Удалить", command=lambda: confirm_delete(found_students, found_exams, select_num))
            delete_button.pack(side=tk.BOTTOM, padx=5, pady=5)
        else:
            return

            

    def delete(self):
        search_option = simpledialog.askinteger("Удаление", "Выберите опцию:\n1. По среднему баллу\n2. По номеру группы\n3. По баллу\n4. По предмету")
        if search_option == 1:
            self.search_by_average_mark(1)
        elif search_option == 2:
            self.search_by_group_number(2)
        elif search_option == 3:
            self.search_by_mark(3)
        elif search_option == 4:
            self.search_by_subject(4)
        else:
            messagebox.showwarning("Ошибка", "Неправильный ввод")

    def prev_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.update_students_list()
            self.update_exams_list()

    def next_page(self):
        if self.current_page < self.max_page:
            self.current_page += 1
            self.update_students_list()
            self.update_exams_list()
