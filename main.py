import tkinter as tk
from tkinter import messagebox, simpledialog

# Базовые данные
users = {}  # Пользователи: {login: {"password": ..., "role": ..., "name": ...}}
students = {}  # Студенты: {id: {"name": ..., "group": ..., "facultatives": {...}}}
facultatives = {}  # Факультативы: {id: {"name": ..., "hours": ..., "type": ...}}
grades = {}  # Оценки: {student_id: {facultative_id: grade}}
schedule = {}  # Расписание: {semestr: {day: {time: facultative_id}}}

# Минимальный объем факультативов для студента
MIN_FACULTATIVE_HOURS = 20

# Главное окно
def main_window():
    def login():
        login_window = tk.Toplevel(window)
        login_window.title("Авторизация")
        login_window.geometry("300x200")

        def authenticate():
            login = entry_login.get()
            password = entry_password.get()
            if login in users and users[login]["password"] == password:
                role = users[login]["role"]
                login_window.destroy()
                if role == "admin":
                    admin_menu()
                elif role == "teacher":
                    teacher_menu()
                elif role == "student":
                    student_menu()
            else:
                messagebox.showerror("Ошибка", "Неверный логин или пароль!")

        label_login = tk.Label(login_window, text="Логин:")
        label_login.pack(pady=5)
        entry_login = tk.Entry(login_window)
        entry_login.pack(pady=5)

        label_password = tk.Label(login_window, text="Пароль:")
        label_password.pack(pady=5)
        entry_password = tk.Entry(login_window, show="*")
        entry_password.pack(pady=5)

        button_auth = tk.Button(login_window, text="Войти", command=authenticate)
        button_auth.pack(pady=10)

    window = tk.Tk()
    window.title("Определение факультативов")
    window.geometry("400x300")

    label = tk.Label(window, text="Система управления факультативами", font=("Arial", 16))
    label.pack(pady=20)

    button_login = tk.Button(window, text="Войти", command=login)
    button_login.pack(pady=20)

    window.mainloop()

# Меню администратора
def admin_menu():
    def back():
        admin_window.destroy()
        main_window()

    def manage_users():
        def add_user():
            name = simpledialog.askstring("Добавление пользователя", "Введите ФИО:")
            if not name:
                return
            role = simpledialog.askstring("Добавление пользователя", "Введите роль (admin/teacher/student):").lower()
            if role not in ["admin", "teacher", "student"]:
                messagebox.showerror("Ошибка", "Недопустимая роль!")
                return
            login = simpledialog.askstring("Добавление пользователя", "Введите логин:")
            if login in users:
                messagebox.showerror("Ошибка", "Логин уже занят!")
                return
            password = simpledialog.askstring("Добавление пользователя", "Введите пароль:")
            users[login] = {"password": password, "role": role, "name": name}
            messagebox.showinfo("Успех", f"Пользователь {name} успешно добавлен!")

        def remove_user():
            login = simpledialog.askstring("Удаление пользователя", "Введите логин пользователя для удаления:")
            if login in users:
                del users[login]
                messagebox.showinfo("Успех", "Пользователь успешно удален!")
            else:
                messagebox.showerror("Ошибка", "Пользователь не найден!")

        user_window = tk.Toplevel(admin_window)
        user_window.title("Управление пользователями")
        user_window.geometry("400x300")

        label_title = tk.Label(user_window, text="Управление пользователями", font=("Arial", 14))
        label_title.pack(pady=10)

        button_add = tk.Button(user_window, text="Добавить пользователя", command=add_user)
        button_add.pack(pady=10)

        button_remove = tk.Button(user_window, text="Удалить пользователя", command=remove_user)
        button_remove.pack(pady=10)

        button_back = tk.Button(user_window, text="Назад", command=lambda: user_window.destroy())
        button_back.pack(pady=20)

    def create_schedule():
        semestr = simpledialog.askinteger("Создание расписания", "Введите номер семестра:")
        day = simpledialog.askstring("Создание расписания", "Введите день недели:")
        time = simpledialog.askstring("Создание расписания", "Введите время:")
        facultative_id = simpledialog.askstring("Создание расписания", "Введите ID факультатива:")
        if semestr not in schedule:
            schedule[semestr] = {}
        if day not in schedule[semestr]:
            schedule[semestr][day] = {}
        schedule[semestr][day][time] = facultative_id
        messagebox.showinfo("Успех", "Расписание успешно создано!")

    def check_min_hours():
        report_window = tk.Toplevel(admin_window)
        report_window.title("Контроль минимального объема факультативов")
        report_window.geometry("600x400")

        group_filter = simpledialog.askstring("Фильтр", "Введите группу для фильтрации (оставьте пустым для всех):")

        text_area = tk.Text(report_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        for student_id, data in students.items():
            if group_filter and data.get("group") != group_filter:
                continue
            total_hours = sum(facultatives[f]["hours"] for f in data.get("facultatives", []))
            status = "OK" if total_hours >= MIN_FACULTATIVE_HOURS else "!!!"
            text_area.insert(tk.END, f"{data['name']} ({data.get('group', '-')}) - {total_hours} часов [{status}]\n")
            if status == "!!!":
                text_area.tag_add("highlight", f"{text_area.index('end')}-2l", f"{text_area.index('end')}-1l")
                text_area.tag_config("highlight", background="red", foreground="white")

        button_back = tk.Button(report_window, text="Назад", command=lambda: report_window.destroy())
        button_back.pack(pady=10)

    admin_window = tk.Tk()
    admin_window.title("Меню администратора")
    admin_window.geometry("400x300")

    label = tk.Label(admin_window, text="Меню администратора", font=("Arial", 16))
    label.pack(pady=20)

    button_manage_users = tk.Button(admin_window, text="Управление пользователями", command=manage_users)
    button_manage_users.pack(pady=10)

    button_create_schedule = tk.Button(admin_window, text="Создание расписания факультативов", command=create_schedule)
    button_create_schedule.pack(pady=10)

    button_check_hours = tk.Button(admin_window, text="Контроль минимального объема факультативов", command=check_min_hours)
    button_check_hours.pack(pady=10)

    button_back = tk.Button(admin_window, text="Назад", command=back)
    button_back.pack(pady=20)

    admin_window.mainloop()

# Меню преподавателя (уже с добавленной функцией ввода оценок)
def teacher_menu():
    def back():
        teacher_window.destroy()
        main_window()

    def view_facultatives():
        if not facultatives:
            messagebox.showinfo("Факультативы", "Нет доступных факультативов.")
            return

        facultative_window = tk.Toplevel(teacher_window)
        facultative_window.title("Мои факультативы")
        facultative_window.geometry("800x400")

        table = tk.Text(facultative_window, wrap=tk.NONE)
        table.pack(fill=tk.BOTH, expand=True)

        table.insert(tk.END, f"{'ID':<10}{'Название':<30}{'Преподаватель':<20}{'Часы':<10}{'Тип':<15}{'Время':<15}\n")
        table.insert(tk.END, "-" * 100 + "\n")

        for fid, data in facultatives.items():
            table.insert(tk.END,
                         f"{fid:<10}{data['name']:<30}{data['teacher']:<20}{data['hours']:<10}{data['type']:<15}{data['time']:<15}\n")

        def add_new():
            add_facultative_window = tk.Toplevel(facultative_window)
            add_facultative_window.title("Добавление факультатива")
            add_facultative_window.geometry("500x400")

            label_id = tk.Label(add_facultative_window, text="ID факультатива:")
            label_id.pack(pady=5)
            entry_id = tk.Entry(add_facultative_window)
            entry_id.pack(pady=5)

            label_name = tk.Label(add_facultative_window, text="Название:")
            label_name.pack(pady=5)
            entry_name = tk.Entry(add_facultative_window)
            entry_name.pack(pady=5)

            label_teacher = tk.Label(add_facultative_window, text="Преподаватель:")
            label_teacher.pack(pady=5)
            entry_teacher = tk.Entry(add_facultative_window)
            entry_teacher.pack(pady=5)

            label_hours = tk.Label(add_facultative_window, text="Количество часов:")
            label_hours.pack(pady=5)
            entry_hours = tk.Entry(add_facultative_window)
            entry_hours.pack(pady=5)

            label_type = tk.Label(add_facultative_window, text="Тип (лекция/практика/лабораторная):")
            label_type.pack(pady=5)
            entry_type = tk.Entry(add_facultative_window)
            entry_type.pack(pady=5)

            label_time = tk.Label(add_facultative_window, text="Время занятия:")
            label_time.pack(pady=5)
            entry_time = tk.Entry(add_facultative_window)
            entry_time.pack(pady=5)

            def save():
                fid = entry_id.get()
                name = entry_name.get()
                teacher = entry_teacher.get()
                hours = entry_hours.get()
                type_ = entry_type.get()
                time = entry_time.get()

                if not all([fid, name, teacher, hours, type_, time]):
                    messagebox.showerror("Ошибка", "Все поля обязательны!")
                    return
                try:
                    hours = int(hours)
                except ValueError:
                    messagebox.showerror("Ошибка", "Часы должны быть числом!")
                    return

                facultatives[fid] = {
                    "name": name,
                    "teacher": teacher,
                    "hours": hours,
                    "type": type_,
                    "time": time
                }
                messagebox.showinfo("Успех", "Факультатив успешно добавлен!")
                add_facultative_window.destroy()
                facultative_window.destroy()
                view_facultatives()

            button_save = tk.Button(add_facultative_window, text="Сохранить", command=save)
            button_save.pack(pady=10)

            button_back = tk.Button(add_facultative_window, text="Отмена", command=add_facultative_window.destroy)
            button_back.pack(pady=10)

        def delete():
            selected_id = simpledialog.askstring("Удаление", "Введите ID факультатива для удаления:")
            if selected_id in facultatives:
                del facultatives[selected_id]
                messagebox.showinfo("Успех", "Факультатив удален!")
                facultative_window.destroy()
                view_facultatives()
            else:
                messagebox.showerror("Ошибка", "Факультатив не найден!")

        def edit():
            selected_id = simpledialog.askstring("Редактирование", "Введите ID факультатива для редактирования:")
            if selected_id not in facultatives:
                messagebox.showerror("Ошибка", "Факультатив не найден!")
                return

            current = facultatives[selected_id]

            edit_window = tk.Toplevel(facultative_window)
            edit_window.title("Редактирование факультатива")
            edit_window.geometry("500x400")

            label_id = tk.Label(edit_window, text=f"ID: {selected_id}")
            label_id.pack(pady=5)

            label_name = tk.Label(edit_window, text="Название:")
            label_name.pack(pady=5)
            entry_name = tk.Entry(edit_window)
            entry_name.insert(0, current["name"])
            entry_name.pack(pady=5)

            label_teacher = tk.Label(edit_window, text="Преподаватель:")
            label_teacher.pack(pady=5)
            entry_teacher = tk.Entry(edit_window)
            entry_teacher.insert(0, current["teacher"])
            entry_teacher.pack(pady=5)

            label_hours = tk.Label(edit_window, text="Количество часов:")
            label_hours.pack(pady=5)
            entry_hours = tk.Entry(edit_window)
            entry_hours.insert(0, str(current["hours"]))
            entry_hours.pack(pady=5)

            label_type = tk.Label(edit_window, text="Тип (лекция/практика/лабораторная):")
            label_type.pack(pady=5)
            entry_type = tk.Entry(edit_window)
            entry_type.insert(0, current["type"])
            entry_type.pack(pady=5)

            label_time = tk.Label(edit_window, text="Время занятия:")
            label_time.pack(pady=5)
            entry_time = tk.Entry(edit_window)
            entry_time.insert(0, current["time"])
            entry_time.pack(pady=5)

            def save_edit():
                name = entry_name.get()
                teacher = entry_teacher.get()
                hours = entry_hours.get()
                type_ = entry_type.get()
                time = entry_time.get()

                if not all([name, teacher, hours, type_, time]):
                    messagebox.showerror("Ошибка", "Все поля обязательны!")
                    return
                try:
                    hours = int(hours)
                except ValueError:
                    messagebox.showerror("Ошибка", "Часы должны быть числом!")
                    return

                facultatives[selected_id] = {
                    "name": name,
                    "teacher": teacher,
                    "hours": hours,
                    "type": type_,
                    "time": time
                }

                messagebox.showinfo("Успех", "Данные обновлены!")
                edit_window.destroy()
                facultative_window.destroy()
                view_facultatives()

            button_save = tk.Button(edit_window, text="Сохранить изменения", command=save_edit)
            button_save.pack(pady=10)

            button_back = tk.Button(edit_window, text="Отмена", command=edit_window.destroy)
            button_back.pack(pady=10)

        def enter_grades():
            grade_window = tk.Toplevel(teacher_window)
            grade_window.title("Ввод оценок")
            grade_window.geometry("400x300")

            label_title = tk.Label(grade_window, text="Ввод оценок студентам", font=("Arial", 14))
            label_title.pack(pady=10)

            # Поле для ID студента
            label_student_id = tk.Label(grade_window, text="Введите ID студента:")
            label_student_id.pack(pady=5)
            entry_student_id = tk.Entry(grade_window)
            entry_student_id.pack(pady=5)

            # Поле для ID факультатива
            label_facultative_id = tk.Label(grade_window, text="Введите ID факультатива:")
            label_facultative_id.pack(pady=5)
            entry_facultative_id = tk.Entry(grade_window)
            entry_facultative_id.pack(pady=5)

            # Поле для оценки
            label_grade = tk.Label(grade_window, text="Введите оценку:")
            label_grade.pack(pady=5)
            entry_grade = tk.Entry(grade_window)
            entry_grade.pack(pady=5)

            # Метка для вывода ошибок или успеха
            result_label = tk.Label(grade_window, text="", fg="red")
            result_label.pack(pady=10)

            def save_grade():
                student_id = entry_student_id.get().strip()
                facultative_id = entry_facultative_id.get().strip()
                grade = entry_grade.get().strip()

                if not student_id or not facultative_id or not grade:
                    result_label.config(text="Все поля обязательны!")
                    return

                if facultative_id not in facultatives:
                    result_label.config(text="Факультатив не найден!")
                    return

                # Инициализируем словарь для студента, если его ещё нет
                if student_id not in grades:
                    grades[student_id] = {}

                # Сохраняем оценку
                grades[student_id][facultative_id] = grade
                result_label.config(text="Оценка успешно добавлена!", fg="green")

            # Кнопка сохранения
            button_save = tk.Button(grade_window, text="Сохранить оценку", command=save_grade)
            button_save.pack(pady=10)

            # Кнопка назад
            button_back = tk.Button(grade_window, text="Закрыть", command=grade_window.destroy)
            button_back.pack(pady=10)

        button_add = tk.Button(facultative_window, text="Добавить факультатив", command=add_new)
        button_add.pack(side=tk.LEFT, padx=10, pady=10)

        button_delete = tk.Button(facultative_window, text="Удалить факультатив", command=delete)
        button_delete.pack(side=tk.LEFT, padx=10, pady=10)

        button_edit = tk.Button(facultative_window, text="Редактировать факультатив", command=edit)
        button_edit.pack(side=tk.LEFT, padx=10, pady=10)

        button_enter_grade = tk.Button(facultative_window, text="Ввести оценку студенту", command=enter_grades)
        button_enter_grade.pack(side=tk.LEFT, padx=10, pady=10)

        button_back = tk.Button(facultative_window, text="Назад", command=facultative_window.destroy)
        button_back.pack(side=tk.BOTTOM, pady=10)

    teacher_window = tk.Tk()
    teacher_window.title("Меню преподавателя")
    teacher_window.geometry("400x300")

    label = tk.Label(teacher_window, text="Меню преподавателя", font=("Arial", 16))
    label.pack(pady=20)

    button_view_facultatives = tk.Button(teacher_window, text="Посмотреть/редактировать факультативы", command=view_facultatives)
    button_view_facultatives.pack(pady=10)

    button_back = tk.Button(teacher_window, text="Назад", command=back)
    button_back.pack(pady=20)

    teacher_window.mainloop()

# Меню студента
def student_menu():
    def back():
        student_window.destroy()
        main_window()

    def view_facultatives():
        messagebox.showinfo("Доступные факультативы", str(facultatives))

    def enroll_facultative():
        facultative_id = simpledialog.askstring("Запись на факультатив", "Введите ID факультатива:")
        if facultative_id in facultatives:
            student_id = simpledialog.askstring("Запись на факультатив", "Введите ваш ID:")
            if student_id not in students:
                students[student_id] = {"facultatives": []}
            students[student_id]["facultatives"].append(facultative_id)
            messagebox.showinfo("Запись на факультатив", "Вы успешно записались!")
        else:
            messagebox.showerror("Ошибка", "Факультатив не найден!")

    student_window = tk.Tk()
    student_window.title("Меню студента")
    student_window.geometry("400x300")

    label = tk.Label(student_window, text="Меню студента", font=("Arial", 16))
    label.pack(pady=20)

    button_view_facultatives = tk.Button(student_window, text="Просмотр доступных факультативов", command=view_facultatives)
    button_view_facultatives.pack(pady=10)

    button_enroll = tk.Button(student_window, text="Запись на факультатив", command=enroll_facultative)
    button_enroll.pack(pady=10)

    button_back = tk.Button(student_window, text="Назад", command=back)
    button_back.pack(pady=20)

    student_window.mainloop()

# Запуск программы
if __name__ == "__main__":
    # Добавление начальных пользователей
    users["admin"] = {"password": "admin", "role": "admin", "name": "Администратор"}
    users["teacher1"] = {"password": "teacher1", "role": "teacher", "name": "Преподаватель 1"}
    users["student1"] = {"password": "student1", "role": "student", "name": "Студент 1"}

    # Добавление начальных факультативов
    facultatives["1"] = {"name": "Математика", "teacher": "Иванов И.И.", "hours": 20, "type": "Лекция", "time": "10:00"}
    facultatives["2"] = {"name": "Программирование", "teacher": "Петров П.П.", "hours": 30, "type": "Практика", "time": "12:00"}

    main_window()