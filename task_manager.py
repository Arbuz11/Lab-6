class TaskManager:
    def __init__(self, database):
        self.database = database

    def add_task(self, task):
        return self.database.add_task(task)

    def get_all_tasks(self):
        return self.database.get_all_tasks()

    def update_task(self, task):
        self.database.update_task(task)

    def delete_task(self, task_id):
        self.database.delete_task(task_id)