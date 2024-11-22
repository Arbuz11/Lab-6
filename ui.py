import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime

class GUI:
    def __init__(self, task_manager):
        self.task_manager = task_manager
        self.root = tk.Tk()
        self.root.title("Менеджер задач")
        self.root.geometry("600x400")

    def create_main_window(self):
        self.create_task_list()
        self.create_buttons()
        self.root.mainloop()

    def create_task_list(self):
        self.tree = ttk.Treeview(self.root, columns=('ID', 'Название', 'Описание', 'Дата', 'Статус'), show='headings')
        self.tree.heading('ID', text='ID')
        self.tree.heading('Название', text='Название')
        self.tree.heading('Описание', text='Описание')
        self.tree.heading('Дата', text='Дата')
        self.tree.heading('Статус', text='Статус')
        self.tree.pack(fill=tk.BOTH, expand=1)
        self.refresh_task_list()

    def create_buttons(self):
        frame = tk.Frame(self.root)
        frame.pack(pady=10)

        add_button = tk.Button(frame, text="Добавить задачу", command=self.create_add_task_window)
        add_button.pack(side=tk.LEFT, padx=5)

        edit_button = tk.Button(frame, text="Редактировать задачу", command=self.edit_selected_task)
        edit_button.pack(side=tk.LEFT, padx=5)

        delete_button = tk.Button(frame, text="Удалить задачу", command=self.delete_selected_task)
        delete_button.pack(side=tk.LEFT, padx=5)

    def refresh_task_list(self):
        for i in self.tree.get_children():
            self.tree.delete(i)

        tasks = self.task_manager.get_all_tasks()
        for task in tasks:
            status = "Выполнено" if task[4] else "Не выполнено"
            self.tree.insert('', 'end', values=(task[0], task[1], task[2], task[3], status))

    def create_add_task_window(self):
        add_window = tk.Toplevel(self.root)
        add_window.title("Добавить задачу")
        add_window.geometry("300x250")

        tk.Label(add_window, text="Название:").pack()
        title_entry = tk.Entry(add_window)
        title_entry.pack()

        tk.Label(add_window, text="Описание:").pack()
        description_entry = tk.Entry(add_window)
        description_entry.pack()

        tk.Label(add_window, text="Дата выполнения:").pack()
        date_entry = DateEntry(add_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.pack()

        status_var = tk.BooleanVar()
        status_check = tk.Checkbutton(add_window, text="Выполнено", variable=status_var)
        status_check.pack()

        def save_task():
            title = title_entry.get()
            description = description_entry.get()
            due_date = date_entry.get_date().strftime("%Y-%m-%d")
            status = status_var.get()

            if not title:
                messagebox.showerror("Ошибка", "Название задачи не может быть пустым")
                return

            task = {
                'title': title,
                'description': description,
                'due_date': due_date,
                'status': int(status)
            }
            self.task_manager.add_task(task)
            self.refresh_task_list()
            add_window.destroy()

        save_button = tk.Button(add_window, text="Сохранить", command=save_task)
        save_button.pack(pady=10)

    def edit_selected_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите задачу для редактирования")
            return

        task_id = self.tree.item(selected_item)['values'][0]
        task = next((task for task in self.task_manager.get_all_tasks() if task[0] == task_id), None)

        if not task:
            messagebox.showerror("Ошибка", "Задача не найдена")
            return

        edit_window = tk.Toplevel(self.root)
        edit_window.title("Редактировать задачу")
        edit_window.geometry("300x250")

        tk.Label(edit_window, text="Название:").pack()
        title_entry = tk.Entry(edit_window)
        title_entry.insert(0, task[1])
        title_entry.pack()

        tk.Label(edit_window, text="Описание:").pack()
        description_entry = tk.Entry(edit_window)
        description_entry.insert(0, task[2])
        description_entry.pack()

        tk.Label(edit_window, text="Дата выполнения:").pack()
        date_entry = DateEntry(edit_window, width=12, background='darkblue', foreground='white', borderwidth=2)
        date_entry.set_date(datetime.strptime(task[3], "%Y-%m-%d").date())
        date_entry.pack()

        status_var = tk.BooleanVar(value=bool(task[4]))
        status_check = tk.Checkbutton(edit_window, text="Выполнено", variable=status_var)
        status_check.pack()

        def save_edited_task():
            title = title_entry.get()
            description = description_entry.get()
            due_date = date_entry.get_date().strftime("%Y-%m-%d")
            status = status_var.get()

            if not title:
                messagebox.showerror("Ошибка", "Название задачи не может быть пустым")
                return

            edited_task = {
                'id': task_id,
                'title': title,
                'description': description,
                'due_date': due_date,
                'status': int(status)
            }
            self.task_manager.update_task(edited_task)
            self.refresh_task_list()
            edit_window.destroy()

        save_button = tk.Button(edit_window, text="Сохранить", command=save_edited_task)
        save_button.pack(pady=10)

    def delete_selected_task(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Ошибка", "Выберите задачу для удаления")
            return

        task_id = self.tree.item(selected_item)['values'][0]
        confirm = messagebox.askyesno("Подтверждение", "Вы уверены, что хотите удалить эту задачу?")

        if confirm:
            self.task_manager.delete_task(task_id)
            self.refresh_task_list()