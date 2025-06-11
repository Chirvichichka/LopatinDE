from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import joinedload

from database.database import Database
from database.models import Material, Product, material_product, ProductType, MaterialType


class MaterialService:
    def __init__(self, db: Database):
        self.db = db

    def get_all_material_types(self):
        """Получение всех типов материалов"""
        try:
            with self.db.get_session() as session:
                return session.query(MaterialType).all()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении типов материалов: {e}")
            return []

    def get_all_materials(self):
        """Получение всех материалов"""
        try:
            with self.db.get_session() as session:
                materials = session.query(Material).options(joinedload(Material.type)).all()
                print(f"Получено материалов из БД: {len(materials)}")  # Отладочная информация
                for material in materials:
                    print(f"Материал в БД: {material.name}, ID: {material.id}")  # Отладочная информация
                return materials
        except SQLAlchemyError as e:
            print(f"Ошибка при получении материалов: {e}")
            return []

    def get_material_by_id(self, material_id: int):
        """Получение материала по ID"""
        try:
            with self.db.get_session() as session:
                return session.query(Material).options(joinedload(Material.type)).filter(
                    Material.id == material_id).first()
        except SQLAlchemyError as e:
            print(f"Ошибка при получении материала: {e}")
            return None

    def add_material(self, material_data: dict):
        """Добавление нового материала"""
        try:
            with self.db.get_session() as session:
                # Получаем тип материала по имени
                material_type = session.query(MaterialType).filter(
                    MaterialType.name == material_data['type_name']
                ).first()

                if not material_type:
                    raise ValueError(f"Тип материала '{material_data['type_name']}' не найден")

                # Создаем новый материал
                material = Material(
                    type_id=material_type.id,
                    name=material_data['name'],
                    price=material_data['price'],
                    unit=material_data['unit'],
                    package_quantity=material_data['package_quantity'],
                    stock_quantity=material_data['stock_quantity'],
                    min_quantity=material_data['min_quantity']
                )

                session.add(material)
                session.commit()
                return material
        except SQLAlchemyError as e:
            print(f"Ошибка при добавлении материала: {e}")
            return None

    def update_material(self, material_id: int, material_data: dict):
        """Обновление материала"""
        try:
            with self.db.get_session() as session:
                material = session.query(Material).filter(Material.id == material_id).first()
                if not material:
                    return None

                # Получаем тип материала по имени
                material_type = session.query(MaterialType).filter(
                    MaterialType.name == material_data['type_name']
                ).first()

                if not material_type:
                    raise ValueError(f"Тип материала '{material_data['type_name']}' не найден")

                # Обновляем данные материала
                material.type_id = material_type.id
                material.name = material_data['name']
                material.price = material_data['price']
                material.unit = material_data['unit']
                material.package_quantity = material_data['package_quantity']
                material.stock_quantity = material_data['stock_quantity']
                material.min_quantity = material_data['min_quantity']

                session.commit()
                return material
        except SQLAlchemyError as e:
            print(f"Ошибка при обновлении материала: {e}")
            return None

    def calculate_required_quantity(self, material_id: int) -> float:
        """Расчет требуемого количества материала"""
        try:
            with self.db.get_session() as session:
                material = session.query(Material).filter(Material.id == material_id).first()
                if not material:
                    return 0.0

                # Получаем все связи материала с продуктами
                material_products = session.query(material_product).filter(
                    material_product.c.material_id == material_id
                ).all()

                total_required = 0.0
                for mp in material_products:
                    # Получаем продукт
                    product = session.query(Product).filter(Product.id == mp.product_id).first()
                    if product and product.quantity:
                        # Умножаем количество материала на количество продукта
                        total_required += mp.quantity * product.quantity

                return total_required
        except SQLAlchemyError as e:
            print(f"Ошибка при расчете требуемого количества: {e}")
            return 0.0

    def get_products_for_material(self, material_id: int):
        """Получение списка продуктов, использующих материал"""
        try:
            with self.db.get_session() as session:
                # Отладочная информация
                print(f"\nПроверка связей для материала ID={material_id}")

                # Проверяем связи напрямую
                material_products = session.query(material_product).filter(
                    material_product.c.material_id == material_id
                ).all()
                print(f"Найдено связей в таблице material_product: {len(material_products)}")
                for mp in material_products:
                    print(f"Связь: material_id={mp.material_id}, product_id={mp.product_id}, quantity={mp.quantity}")

                # Проверяем сам материал
                material = session.query(Material).filter(Material.id == material_id).first()
                if material:
                    print(f"Материал найден: {material.name}")
                    print(f"Количество связанных продуктов: {len(material.products)}")
                else:
                    print("Материал не найден!")

                # Получаем продукты
                products = session.query(Product).options(
                    joinedload(Product.type)
                ).join(Product.materials).filter(Material.id == material_id).all()

                print(f"Запрос вернул продуктов: {len(products)}")
                return products

        except SQLAlchemyError as e:
            print(f"Ошибка при получении продуктов: {e}")
            return []

    def calculate_product_quantity(self, product_type_id, material_quantity, param1, param2):
        """Расчет количества получаемой продукции"""
        try:
            with self.db.get_session() as session:
                # Проверка существования типов продукции и материала
                product_type = session.query(ProductType).filter(
                    ProductType.id == product_type_id
                ).first()

                if not product_type:
                    return -1

                # Расчет количества продукции
                material_per_product = param1 * param2 * product_type.coefficient
                if material_per_product <= 0:
                    return -1

                # Учет потерь материала
                loss_percentage = 0.05
                effective_quantity = material_quantity * (1 - loss_percentage)

                # Расчет итогового количества продукции
                product_quantity = effective_quantity / material_per_product
                return product_quantity

        except Exception:
            return -1