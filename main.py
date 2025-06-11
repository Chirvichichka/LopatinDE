import tkinter as tk
from database.database import Database
from business.material_service import MaterialService
from gui.main_window import MainWindow
from database.load_data import load_all_data
import os


def main():
    # Проверяем, существует ли база данных
    if not os.path.exists("materials.db"):
        print("База данных не найдена. Начинаем загрузку данных...")
        load_all_data()

    # Инициализация базы данных
    db = Database()
    print("База данных инициализирована")

    # Создание сервиса для работы с материалами
    material_service = MaterialService(db)
    print("Сервис материалов создан")

    # Создание главного окна
    root = tk.Tk()
    app = MainWindow(root, material_service)
    print("Главное окно создано")

    # Запуск главного цикла приложения
    root.app = app
    root.mainloop()


if __name__ == "__main__":
    main()
