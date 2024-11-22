from database import Database
from task_manager import TaskManager
from ui import GUI

def main():
    db = Database()
    task_manager = TaskManager(db)
    gui = GUI(task_manager)
    gui.create_main_window()

if __name__ == "__main__":
    main()
