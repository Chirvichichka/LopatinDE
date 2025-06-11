import pandas as pd
import os
from sqlalchemy.exc import SQLAlchemyError
from .database import Database
from .models import MaterialType, Material, ProductType, Product, material_product
from sqlalchemy import func

def load_material_types(db: Database, file_path: str):
    """Загрузка типов материалов из Excel"""
    try:
        print(f"Чтение файла {file_path}...")
        df = pd.read_excel(file_path)
        print(f"Столбцы в файле: {df.columns.tolist()}")
        with db.get_session() as session:
            for _, row in df.iterrows():
                material_type = MaterialType(
                    name=str(row['Тип материала']).strip()
                )
                session.merge(material_type)
            session.commit()
        print(f"Загружено типов материалов: {len(df)}")
    except Exception as e:
        print(f"Ошибка при загрузке типов материалов: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def load_materials(db: Database, file_path: str):
    """Загрузка материалов из Excel"""
    try:
        print(f"Чтение файла {file_path}...")
        df = pd.read_excel(file_path)
        print(f"Столбцы в файле: {df.columns.tolist()}")
        with db.get_session() as session:
            for _, row in df.iterrows():
                material_type = session.query(MaterialType).filter_by(name=str(row['Тип материала']).strip()).first()
                if not material_type:
                    print(f"Тип материала '{row['Тип материала']}' не найден!")
                    continue
                material_name = str(row['Наименование материала']).strip()
                material = session.query(Material).filter_by(name=material_name).first()
                if material:
                    # Обновляем существующий материал
                    material.type_id = material_type.id
                    material.price = float(str(row['Цена единицы материала']).replace(',', '.')) if not pd.isna(
                        row['Цена единицы материала']) else None
                    material.unit = str(row['Единица измерения']).strip() if not pd.isna(
                        row['Единица измерения']) else None
                    material.package_quantity = float(
                        str(row['Количество в упаковке']).replace(',', '.')) if not pd.isna(
                        row['Количество в упаковке']) else None
                    material.stock_quantity = float(str(row['Количество на складе']).replace(',', '.')) if not pd.isna(
                        row['Количество на складе']) else None
                    material.min_quantity = float(str(row['Минимальное количество']).replace(',', '.')) if not pd.isna(
                        row['Минимальное количество']) else None
                else:
                    # Добавляем новый материал
                    material = Material(
                        name=material_name,
                        type_id=material_type.id,
                        price=float(str(row['Цена единицы материала']).replace(',', '.')) if not pd.isna(
                            row['Цена единицы материала']) else None,
                        unit=str(row['Единица измерения']).strip() if not pd.isna(row['Единица измерения']) else None,
                        package_quantity=float(str(row['Количество в упаковке']).replace(',', '.')) if not pd.isna(
                            row['Количество в упаковке']) else None,
                        stock_quantity=float(str(row['Количество на складе']).replace(',', '.')) if not pd.isna(
                            row['Количество на складе']) else None,
                        min_quantity=float(str(row['Минимальное количество']).replace(',', '.')) if not pd.isna(
                            row['Минимальное количество']) else None
                    )
                    session.add(material)
            session.commit()
        print(f"Загружено материалов: {len(df)}")
    except Exception as e:
        print(f"Ошибка при загрузке материалов: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def load_product_types(db: Database, file_path: str):
    """Загрузка типов продукции из Excel"""
    try:
        print(f"Чтение файла {file_path}...")
        df = pd.read_excel(file_path)
        print(f"Столбцы в файле: {df.columns.tolist()}")
        with db.get_session() as session:
            for _, row in df.iterrows():
                product_type = ProductType(
                    name=str(row['Тип продукции']).strip(),
                    coefficient=float(str(row['Коэффициент типа продукции']).replace(',', '.')) if not pd.isna(
                        row['Коэффициент типа продукции']) else None
                )
                session.merge(product_type)
            session.commit()
        print(f"Загружено типов продукции: {len(df)}")
    except Exception as e:
        print(f"Ошибка при загрузке типов продукции: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def load_products(db: Database, file_path: str):
    """Загрузка продукции из Excel"""
    try:
        print(f"Чтение файла {file_path}...")
        df = pd.read_excel(file_path)
        print(f"Столбцы в файле: {df.columns.tolist()}")
        with db.get_session() as session:
            for _, row in df.iterrows():
                product_type = session.query(ProductType).filter_by(name=str(row['Тип продукции']).strip()).first()
                if not product_type:
                    print(f"Тип продукции '{row['Тип продукции']}' не найден!")
                    continue
                product_article = str(row['Артикул']).strip()
                product = session.query(Product).filter_by(article=product_article).first()
                if product:
                    # Обновляем существующий продукт
                    product.name = str(row['Наименование продукции']).strip()
                    product.type_id = product_type.id
                    product.min_partner_price = float(
                        str(row['Минимальная стоимость для партнера']).replace(',', '.')) if not pd.isna(
                        row['Минимальная стоимость для партнера']) else None
                else:
                    # Добавляем новый продукт
                    product = Product(
                        name=str(row['Наименование продукции']).strip(),
                        article=product_article,
                        type_id=product_type.id,
                        min_partner_price=float(
                            str(row['Минимальная стоимость для партнера']).replace(',', '.')) if not pd.isna(
                            row['Минимальная стоимость для партнера']) else None
                    )
                    session.add(product)
            session.commit()
        print(f"Загружено продукции: {len(df)}")
    except Exception as e:
        print(f"Ошибка при загрузке продукции: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def load_material_product_relations(db: Database, file_path: str):
    """Загрузка связей между материалами и продукцией из Excel"""
    try:
        print(f"Чтение файла {file_path}...")
        df = pd.read_excel(file_path)
        # Удаляем пробелы и приводим к нижнему регистру заголовки
        df.columns = [col.strip().lower() for col in df.columns]
        print(f"Столбцы в файле: {df.columns.tolist()}")

        with db.get_session() as session:
            # Очищаем существующие связи
            session.execute(material_product.delete())
            session.commit()

            # Получаем все материалы и создаем словарь для быстрого поиска
            materials = session.query(Material).all()
            material_dict = {material.name.lower().strip(): material for material in materials}

            # Получаем все продукты и создаем словарь для быстрого поиска
            products = session.query(Product).all()
            product_dict = {product.name.lower().strip(): product for product in products}

            for _, row in df.iterrows():
                # Найти материал по наименованию (без учета регистра и пробелов)
                material_name = str(row['наименование материала']).strip().lower()
                material = material_dict.get(material_name)
                if not material:
                    print(f"Материал '{material_name}' не найден!")
                    continue

                # Найти продукт по наименованию (без учета регистра и пробелов)
                product_name = str(row['продукция']).strip().lower()
                product = product_dict.get(product_name)
                if not product:
                    print(f"Продукция '{product_name}' не найдена!")
                    continue

                # Получаем количество материала
                try:
                    quantity = float(str(row['необходимое количество материала']).replace(',', '.'))
                except (ValueError, TypeError):
                    print(f"Некорректное количество материала для связи {material_name} - {product_name}")
                    continue

                # Добавляем связь
                try:
                    session.execute(
                        material_product.insert().values(
                            material_id=material.id,
                            product_id=product.id,
                            quantity=quantity
                        )
                    )
                    print(f"Добавлена связь: {material.name} - {product.name} ({quantity})")
                except Exception as e:
                    print(f"Ошибка при добавлении связи {material_name} - {product_name}: {e}")

            session.commit()
            print(f"Загружено связей материалов с продукцией: {len(df)}")

            # Проверяем загруженные связи
            total_relations = session.query(material_product).count()
            print(f"Всего связей в базе данных: {total_relations}")

    except Exception as e:
        print(f"Ошибка при загрузке связей: {e}")
        import traceback
        print(f"Traceback: {traceback.format_exc()}")


def load_all_data():
    """Загрузка всех данных из Excel-файлов"""
    db = Database()
    db.create_tables()  # Создаём таблицы с нуля
    # Пути к файлам
    material_types_file = "resources/Material_type_import.xlsx"
    materials_file = "resources/Materials_import.xlsx"
    product_types_file = "resources/Product_type_import.xlsx"
    products_file = "resources/Products_import.xlsx"
    material_products_file = "resources/Material_products__import.xlsx"
    print("Начинаем загрузку данных...")
    if os.path.exists(material_types_file):
        print("Загрузка типов материалов...")
        load_material_types(db, material_types_file)
    else:
        print(f"Файл {material_types_file} не найден!")
    if os.path.exists(materials_file):
        print("Загрузка материалов...")
        load_materials(db, materials_file)
    else:
        print(f"Файл {materials_file} не найден!")
    if os.path.exists(product_types_file):
        print("Загрузка типов продукции...")
        load_product_types(db, product_types_file)
    else:
        print(f"Файл {product_types_file} не найден!")
    if os.path.exists(products_file):
        print("Загрузка продукции...")
        load_products(db, products_file)
    else:
        print(f"Файл {products_file} не найден!")
    if os.path.exists(material_products_file):
        print("Загрузка связей материалов с продукцией...")
        load_material_product_relations(db, material_products_file)
    else:
        print(f"Файл {material_products_file} не найден!")
    print("Загрузка данных завершена!")


if __name__ == "__main__":
    load_all_data()