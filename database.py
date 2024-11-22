import sqlite3
from datetime import datetime

class Database:
    def __init__(self):
        self.conn = sqlite3.connect('tasks.db')
        self.cursor = self.conn.cursor()
        self.create_table()

    def create_table(self):
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS tasks (
                id INTEGER PRIMARY KEY,
                title TEXT NOT NULL,
                description TEXT,
                due_date TEXT,
                status INTEGER
            )
        ''')
        self.conn.commit()

    def add_task(self, task):
        self.cursor.execute('''
            INSERT INTO tasks (title, description, due_date, status)
            VALUES (?, ?, ?, ?)
        ''', (task['title'], task['description'], task['due_date'], task['status']))
        self.conn.commit()
        return self.cursor.lastrowid

    def get_all_tasks(self):
        self.cursor.execute('SELECT * FROM tasks')
        return self.cursor.fetchall()

    def update_task(self, task):
        self.cursor.execute('''
            UPDATE tasks
            SET title = ?, description = ?, due_date = ?, status = ?
            WHERE id = ?
        ''', (task['title'], task['description'], task['due_date'], task['status'], task['id']))
        self.conn.commit()

    def delete_task(self, task_id):
        self.cursor.execute('DELETE FROM tasks WHERE id = ?', (task_id,))
        self.conn.commit()

    def __del__(self):
        self.conn.close()