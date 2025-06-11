from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import SQLAlchemyError
from .models import Base


class Database:
    def __init__(self, db_path="sqlite:///materials.db"):
        self.engine = create_engine(db_path)
        self.Session = sessionmaker(bind=self.engine)

    def create_tables(self):
        """Создание всех таблиц в базе данных"""
        Base.metadata.create_all(self.engine)

    def get_session(self):
        """Получение сессии для работы с базой данных"""
        return self.Session()

    def close_session(self, session):
        """Закрытие сессии"""
        session.close()

    def execute_query(self, query_func):
        """Выполнение запроса с обработкой ошибок"""
        session = self.get_session()
        try:
            result = query_func(session)
            session.commit()
            return result
        except SQLAlchemyError as e:
            session.rollback()
            raise e
        finally:
            self.close_session(session)