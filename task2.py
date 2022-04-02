import random

from faker import Faker
from sqlalchemy import Column, Integer, String, create_engine, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db = create_engine('sqlite:///db.sqlite')
Base = declarative_base()


class Clients(Base):
    __tablename__ = 'Clients'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), nullable=False)
    second_name = Column(String(50), nullable=False)
    phone = Column(Integer, nullable=False)
    terms_service = Column(Boolean, nullable=False)
    personal_data = Column(Boolean, nullable=False)
    email = Column(String(50), nullable=False)
    email_spam = Column(Boolean, nullable=False)

    def __repr__(self):
        return f"id: {self.id}, name: {self.name}, second_name: {self.second_name},email: {self.email}" \
               f"phone: {self.phone}, terms_service: {self.terms_service}, personal_data: {self.personal_data}," \
               f"email_spam: {self.email_spam}"


Base.metadata.create_all(db)


def clients_add():
    """Функция заполняющая таблицу рандомными данными"""
    Session = sessionmaker(bind=db)
    session = Session()
    fake = Faker()

    faker_clients = [Clients(
        name=fake.name(),
        second_name=fake.last_name(),
        email=fake.email(),
        phone=fake.phone_number(),
        terms_service=random.choice([True, False]),
        personal_data=random.choice([True, False]),
        email_spam=random.choice([True, False])
    ) for i in range(10)]
    print(faker_clients)
    session.add_all(faker_clients)
    session.commit()
    session.close()


clients_add()
