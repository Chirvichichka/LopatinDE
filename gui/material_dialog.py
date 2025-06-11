import tkinter as tk
from tkinter import ttk, messagebox
from database.models import MaterialType
import os

class MaterialDialog:
    def __init__(self, parent, material_service, material=None):
        self.dialog = tk.Toplevel(parent)
        self.material_service = material_service
        self.material = material

        # Настройка шрифта для диалогового окна
        self.configure_fonts()

        # Настройка окна
        self.dialog.title("Добавление материала" if not material else "Редактирование материала")
        self.dialog.geometry("400x500")
        self.dialog.resizable(False, False)

        # Установка иконки
        if os.path.exists("resources/Образ плюс.ico"):
            self.dialog.iconbitmap("resources/Образ плюс.ico")

        # Создание и размещение элементов
        self.create_widgets()

        # Если материал передан, заполняем поля
        if material:
            self.fill_fields()

    def configure_fonts(self):
        """Настройка шрифтов для диалогового окна"""
        # Настройка стилей ttk
        style = ttk.Style()
        style.configure("Dialog.TLabel", font=("Constantia", 10))
        style.configure("Dialog.TEntry", font=("Constantia", 10))
        style.configure("Dialog.TButton", font=("Constantia", 10))
        style.configure("Dialog.TCombobox", font=("Constantia", 10))

    def create_widgets(self):
        # Фрейм для полей ввода
        input_frame = ttk.Frame(self.dialog, padding="10")
        input_frame.pack(fill=tk.BOTH, expand=True)

        # Тип материала
        ttk.Label(input_frame, text="Тип материала:", style="Dialog.TLabel").grid(row=0, column=0, sticky=tk.W, pady=5)
        self.type_var = tk.StringVar()
        self.type_combo = ttk.Combobox(input_frame, textvariable=self.type_var, style="Dialog.TCombobox")
        self.type_combo.grid(row=0, column=1, sticky=tk.EW, pady=5)
        self.load_material_types()

        # Наименование
        ttk.Label(input_frame, text="Наименование:", style="Dialog.TLabel").grid(row=1, column=0, sticky=tk.W, pady=5)
        self.name_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.name_var, style="Dialog.TEntry").grid(row=1, column=1, sticky=tk.EW, pady=5)

        # Цена
        ttk.Label(input_frame, text="Цена:", style="Dialog.TLabel").grid(row=2, column=0, sticky=tk.W, pady=5)
        self.price_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.price_var, style="Dialog.TEntry").grid(row=2, column=1, sticky=tk.EW, pady=5)

        # Единица измерения
        ttk.Label(input_frame, text="Единица измерения:", style="Dialog.TLabel").grid(row=3, column=0, sticky=tk.W, pady=5)
        self.unit_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.unit_var, style="Dialog.TEntry").grid(row=3, column=1, sticky=tk.EW, pady=5)

        # Количество в упаковке
        ttk.Label(input_frame, text="Количество в упаковке:", style="Dialog.TLabel").grid(row=4, column=0, sticky=tk.W, pady=5)
        self.package_quantity_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.package_quantity_var, style="Dialog.TEntry").grid(row=4, column=1, sticky=tk.EW, pady=5)

        # Количество на складе
        ttk.Label(input_frame, text="Количество на складе:", style="Dialog.TLabel").grid(row=5, column=0, sticky=tk.W, pady=5)
        self.stock_quantity_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.stock_quantity_var, style="Dialog.TEntry").grid(row=5, column=1, sticky=tk.EW, pady=5)

        # Минимальное количество
        ttk.Label(input_frame, text="Минимальное количество:", style="Dialog.TLabel").grid(row=6, column=0, sticky=tk.W, pady=5)
        self.min_quantity_var = tk.StringVar()
        ttk.Entry(input_frame, textvariable=self.min_quantity_var, style="Dialog.TEntry").grid(row=6, column=1, sticky=tk.EW, pady=5)

        # Кнопки
        button_frame = ttk.Frame(self.dialog, padding="10")
        button_frame.pack(fill=tk.X)

        tk.Button(button_frame, text="Сохранить", command=self.save, font=("Constantia", 10), bg="#BFD6F6").pack(side=tk.RIGHT, padx=5)
        tk.Button(button_frame, text="Отмена", command=self.dialog.destroy,  font=("Constantia", 10),  bg="#BFD6F6").pack(side=tk.RIGHT, padx=5)

        # Настройка сетки
        input_frame.columnconfigure(1, weight=1)

    def load_material_types(self):
        """Загрузка типов материалов в выпадающий список"""
        material_types = self.material_service.get_all_material_types()
        self.type_combo['values'] = [mt.name for mt in material_types]
        if material_types:
            self.type_combo.current(0)

    def fill_fields(self):
        """Заполнение полей данными материала"""
        self.type_var.set(self.material.type.name)
        self.name_var.set(self.material.name)
        self.price_var.set(str(self.material.price))
        self.unit_var.set(self.material.unit)
        self.package_quantity_var.set(str(self.material.package_quantity))
        self.stock_quantity_var.set(str(self.material.stock_quantity))
        self.min_quantity_var.set(str(self.material.min_quantity))

    def save(self):
        """Сохранение данных материала"""
        try:
            # Получение данных из полей
            material_data = {
                'type_name': self.type_var.get(),
                'name': self.name_var.get(),
                'price': float(self.price_var.get()),
                'unit': self.unit_var.get(),
                'package_quantity': float(self.package_quantity_var.get()),
                'stock_quantity': float(self.stock_quantity_var.get()),
                'min_quantity': float(self.min_quantity_var.get())
            }

            # Проверка обязательных полей
            if not all([material_data['type_name'], material_data['name'], material_data['unit']]):
                messagebox.showerror("Ошибка", "Заполните все обязательные поля")
                return

            # Сохранение материала
            if self.material:
                self.material_service.update_material(self.material.id, material_data)
            else:
                self.material_service.add_material(material_data)

            self.dialog.destroy()

        except ValueError as e:
            messagebox.showerror("Ошибка", "Введите корректные числовые значения")
        except Exception as e:
            messagebox.showerror("Ошибка", f"Ошибка при сохранении: {str(e)}")