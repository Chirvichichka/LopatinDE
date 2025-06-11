import tkinter as tk
from tkinter import ttk, messagebox
from PIL import Image, ImageTk
import os
from business.material_service import MaterialService
from gui.material_dialog import MaterialDialog
from gui.products_window import ProductsWindow
from database.models import MaterialType


class MainWindow:
    def __init__(self, root, material_service):
        self.root = root
        self.material_service = material_service

        # Настройка шрифта для всего приложения
        self.configure_fonts()

        # Настройка окна
        self.root.title("Система учета материалов")
        self.root.geometry("1000x700")

        # Установка иконки
        if os.path.exists("resources/Образ плюс.ico"):
            self.root.iconbitmap("resources/Образ плюс.ico")

        # Установка логотипа
        if os.path.exists("resources/Образ плюс.png"):
            logo_img = Image.open("resources/Образ плюс.png")
            logo_img = logo_img.resize((100, 100), Image.Resampling.LANCZOS)
            self.logo = ImageTk.PhotoImage(logo_img)
            logo_label = tk.Label(root, image=self.logo)
            logo_label.pack(pady=10)

            self.title = tk.Label(root, text="Образ плюс", fg = "#405C73")
            self.title.configure(font=("Constantia", 24, "bold"))
            self.title.pack(pady=10)

        # Создание основного контейнера
        self.main_frame = ttk.Frame(root)
        self.main_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Инициализация переменных для поиска
        self.name_search_var = tk.StringVar()
        self.type_search_var = tk.StringVar()
        self.min_quantity_var = tk.StringVar()
        self.max_quantity_var = tk.StringVar()

        # Создание панели поиска
        self.create_search_panel()

        # Создание таблицы материалов
        self.create_materials_table()

        # Создание кнопок
        self.create_buttons()

        # Загрузка данных
        self.load_materials()

        # Привязка событий изменения фильтров
        self.name_search_var.trace('w', self.apply_filters)
        self.type_search_var.trace('w', self.apply_filters)
        self.min_quantity_var.trace('w', self.apply_filters)
        self.max_quantity_var.trace('w', self.apply_filters)

    def configure_fonts(self):
        """Настройка шрифтов для всего приложения"""
        # Настройка стилей ttk
        style = ttk.Style()
        style.configure(".", font=("Constantia", 10))  # Основной шрифт для всех виджетов
        style.configure("Treeview", font=("Constantia", 10))  # Шрифт для таблицы
        style.configure("Treeview.Heading", font=("Constantia", 10, "bold"))  # Шрифт для заголовков таблицы
        style.configure("TLabel", font=("Constantia", 10))  # Шрифт для меток
        style.configure("TButton", font=("Constantia", 10))  # Шрифт для кнопок
        style.configure("TEntry", font=("Constantia", 10))  # Шрифт для полей ввода
        style.configure("TCombobox", font=("Constantia", 10))  # Шрифт для выпадающих списков
        style.configure("TLabelframe.Label", font=("Constantia", 10))  # Шрифт для заголовков фреймов

        # Настройка шрифта для меню
        self.root.option_add("*Menu.font", ("Constantia", 10))

    def create_search_panel(self):
        # Создание фрейма для поиска
        search_frame = ttk.LabelFrame(self.main_frame, text="Поиск и фильтрация")
        search_frame.pack(fill=tk.X, pady=5)

        # Поле поиска по наименованию
        ttk.Label(search_frame, text="Наименование:").grid(row=0, column=0, padx=5, pady=5)
        ttk.Entry(search_frame, textvariable=self.name_search_var).grid(row=0, column=1, padx=5, pady=5)

        # Выпадающий список типов материалов
        ttk.Label(search_frame, text="Тип материала:").grid(row=0, column=2, padx=5, pady=5)
        self.type_combo = ttk.Combobox(search_frame, textvariable=self.type_search_var)
        self.type_combo.grid(row=0, column=3, padx=5, pady=5)
        self.load_material_types()

        # Фильтр по количеству на складе
        ttk.Label(search_frame, text="Количество на складе:").grid(row=1, column=0, padx=5, pady=5)
        self.quantity_frame = ttk.Frame(search_frame)
        self.quantity_frame.grid(row=1, column=1, columnspan=3, padx=5, pady=5)

        ttk.Entry(self.quantity_frame, textvariable=self.min_quantity_var, width=10).pack(side=tk.LEFT)
        ttk.Label(self.quantity_frame, text=" - ").pack(side=tk.LEFT)
        ttk.Entry(self.quantity_frame, textvariable=self.max_quantity_var, width=10).pack(side=tk.LEFT)

        # Кнопка сброса фильтров
        tk.Button(search_frame, text="Сбросить фильтры",  font=("Constantia", 10), command=self.reset_filters, bg="#BFD6F6").grid(row=1, column=4, padx=5,
                                                                                           pady=5)

    def create_materials_table(self):
        # Создание фрейма для таблицы
        table_frame = ttk.Frame(self.main_frame)
        table_frame.pack(fill=tk.BOTH, expand=True)

        # Создание таблицы
        columns = ("id", "type", "name", "price", "unit", "package_quantity",
                   "stock_quantity", "min_quantity")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Настройка заголовков
        self.tree.heading("id", text="ID")
        self.tree.heading("type", text="Тип")
        self.tree.heading("name", text="Наименование")
        self.tree.heading("price", text="Цена")
        self.tree.heading("unit", text="Ед. изм.")
        self.tree.heading("package_quantity", text="Кол-во в упаковке")
        self.tree.heading("stock_quantity", text="На складе")
        self.tree.heading("min_quantity", text="Мин. кол-во")

        # Настройка ширины колонок
        for col in columns:
            self.tree.column(col, width=100)

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещение таблицы и скроллбара
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Привязка событий
        self.tree.bind("<Double-1>", self.on_material_double_click)
        self.tree.bind("<Button-3>", self.show_context_menu)

    def create_buttons(self):
        # Создание фрейма для кнопок
        button_frame = ttk.Frame(self.main_frame)
        button_frame.pack(fill=tk.X, pady=10)

        # Создание кнопок
        add_button = tk.Button(button_frame, text="Добавить", font=("Constantia", 10), command=self.add_material, bg="#BFD6F6")
        add_button.pack(side=tk.LEFT, padx=5)

        refresh_button = tk.Button(button_frame, text="Обновить", font=("Constantia", 10), command=self.load_materials, bg="#BFD6F6")
        refresh_button.pack(side=tk.LEFT, padx=5)

    def load_material_types(self):
        """Загрузка типов материалов в выпадающий список"""
        material_types = self.material_service.get_all_material_types()
        self.type_combo['values'] = [''] + [mt.name for mt in material_types]
        self.type_combo.current(0)

    def load_materials(self):
        """Загрузка материалов с учетом фильтров"""
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Загрузка материалов
        materials = self.material_service.get_all_materials()
        print(f"Загружено материалов: {len(materials)}")  # Отладочная информация

        # Применение фильтров
        filtered_materials = self.filter_materials(materials)
        print(f"Отфильтровано материалов: {len(filtered_materials)}")  # Отладочная информация

        # Отображение отфильтрованных материалов
        for material in filtered_materials:
            self.tree.insert("", tk.END, values=(
                material.id,
                material.type.name,
                material.name,
                f"{material.price:.2f}",
                material.unit,
                f"{material.package_quantity:.2f}",
                f"{material.stock_quantity:.2f}",
                f"{material.min_quantity:.2f}"
            ))

    def filter_materials(self, materials):
        """Фильтрация материалов по заданным критериям"""
        filtered = materials

        # Фильтр по наименованию
        name_filter = self.name_search_var.get().strip().lower()
        if name_filter:
            filtered = [m for m in filtered if name_filter in m.name.lower()]

        # Фильтр по типу
        type_filter = self.type_search_var.get()
        if type_filter:
            filtered = [m for m in filtered if m.type.name == type_filter]

        # Фильтр по количеству на складе
        try:
            min_qty = float(self.min_quantity_var.get()) if self.min_quantity_var.get() else None
            max_qty = float(self.max_quantity_var.get()) if self.max_quantity_var.get() else None

            if min_qty is not None:
                filtered = [m for m in filtered if m.stock_quantity >= min_qty]
            if max_qty is not None:
                filtered = [m for m in filtered if m.stock_quantity <= max_qty]
        except ValueError:
            pass

        return filtered

    def apply_filters(self, *args):
        """Применение фильтров при изменении значений"""
        self.load_materials()

    def reset_filters(self):
        """Сброс всех фильтров"""
        self.name_search_var.set("")
        self.type_search_var.set("")
        self.min_quantity_var.set("")
        self.max_quantity_var.set("")
        self.load_materials()

    def add_material(self):
        """Открытие окна добавления материала"""
        dialog = MaterialDialog(self.root, self.material_service)
        self.root.wait_window(dialog.dialog)
        self.load_materials()

    def on_material_double_click(self, event):
        """Обработка двойного клика по материалу"""
        item = self.tree.selection()[0]
        material_id = self.tree.item(item)["values"][0]
        material = self.material_service.get_material_by_id(material_id)

        if material:
            dialog = MaterialDialog(self.root, self.material_service, material)
            self.root.wait_window(dialog.dialog)
            self.load_materials()

    def show_context_menu(self, event):
        """Показ контекстного меню"""
        item = self.tree.identify_row(event.y)
        if item:
            self.tree.selection_set(item)
            material_id = self.tree.item(item)["values"][0]
            material = self.material_service.get_material_by_id(material_id)

            menu = tk.Menu(self.root, tearoff=0)
            menu.add_command(label="Редактировать", command=lambda: self.on_material_double_click(None))
            menu.add_command(label="Показать продукцию",
                             command=lambda: ProductsWindow(self.root, self.material_service, material))
            menu.post(event.x_root, event.y_root)