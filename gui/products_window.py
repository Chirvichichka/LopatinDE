import tkinter as tk
from tkinter import ttk

from database.models import material_product


class ProductsWindow:
    def __init__(self, parent, material_service, material):
        self.window = tk.Toplevel(parent)
        self.material_service = material_service
        self.material = material

        # Настройка шрифта для окна продуктов
        self.configure_fonts()

        # Настройка окна
        self.window.title(f"Продукция, использующая материал: {material.name}")
        self.window.geometry("900x500")

        # Создание таблицы
        self.create_products_table()

        # Загрузка данных
        self.load_products()

    def configure_fonts(self):
        """Настройка шрифтов для окна продуктов"""
        # Настройка стилей ttk
        style = ttk.Style()
        style.configure("Products.Treeview", font=("Constantia", 10))
        style.configure("Products.Treeview.Heading", font=("Constantia", 10, "bold"))

    def create_products_table(self):
        # Создание фрейма для таблицы
        table_frame = ttk.Frame(self.window)
        table_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Создание таблицы
        columns = ("id", "name", "article", "type", "quantity", "material_quantity")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings", style="Products.Treeview")

        # Настройка заголовков
        self.tree.heading("id", text="ID")
        self.tree.heading("name", text="Наименование")
        self.tree.heading("article", text="Артикул")
        self.tree.heading("type", text="Тип продукции")
        self.tree.heading("quantity", text="Количество продукции")
        self.tree.heading("material_quantity", text="Расход материала")

        # Настройка ширины колонок
        self.tree.column("id", width=50)
        self.tree.column("name", width=200)
        self.tree.column("article", width=100)
        self.tree.column("type", width=150)
        self.tree.column("quantity", width=150)
        self.tree.column("material_quantity", width=150)

        # Добавление скроллбара
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        # Размещение таблицы и скроллбара
        self.tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def load_products(self):
        # Очистка таблицы
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Загрузка продукции
        products = self.material_service.get_products_for_material(self.material.id)
        print(f"Загружено продуктов для материала {self.material.name}: {len(products)}")

        with self.material_service.db.get_session() as session:
            for product in products:
                print(f"Обработка продукта: {product.name}, ID: {product.id}")
                # Получение количества материала для данной продукции
                material_quantity = session.query(
                    material_product.c.quantity
                ).filter(
                    material_product.c.material_id == self.material.id,
                    material_product.c.product_id == product.id
                ).scalar()

                print(f"Количество материала для продукта {product.name}: {material_quantity}")

                self.tree.insert("", tk.END, values=(
                    product.id,
                    product.name,
                    product.article,
                    product.type.name if product.type else "Не указан",
                    f"{self.material_service.calculate_product_quantity(product.type.id, material_quantity, 1, 1):.2f}",
                    f"{material_quantity:.2f} {self.material.unit}"
                ))