from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, DateTime

Base = declarative_base()


class User(Base):
    __tablename__ = 'test_users'
    __table_arg__ = {'mysql_charset': 'utf8'}

    def __repr__(self):
        return f'{self.__tablename__} row: id={self.id}, username={self.username}, password={self.password}'

    id = Column(Integer, primary_key=True, autoincrement=True, nullable=False)
    name = Column(String(255), nullable=False)
    surname = Column(String(255), nullable=False)
    middle_name = Column(String(255), default=None)
    username = Column(String(16), unique=True, nullable=False)
    password = Column(String(255), nullable=False)
    email = Column(String(64), unique=True, nullable=False)
    access = Column(Integer, default=1)
    active = Column(Integer, default=0)
    start_active_time = Column(DateTime, default=None)
