from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, CHAR

Base = declarative_base()


class TaskBase(Base):
    __tablename__ = None
    __table_arg__ = {'mysql_charset': 'utf8'}
    __abstract__ = True

    def __repr__(self):
        return f'{self.__tablename__} row: id={self.id}'

    id = Column(Integer, primary_key=True, autoincrement=True)
    amount = Column(Integer, nullable=False)


class Task1(TaskBase):
    __tablename__ = 'Task1'


class Task2(TaskBase):
    __tablename__ = 'Task2'

    method = Column(CHAR(255), nullable=False)


class Task3(TaskBase):
    __tablename__ = 'Task3'

    url = Column(CHAR(50), nullable=False)


class Task4(TaskBase):
    __tablename__ = 'Task4'

    url = Column(CHAR(255), nullable=False)
    status = Column(Integer, nullable=False)
    ip = Column(CHAR(50), nullable=False)


class Task5(TaskBase):
    __tablename__ = 'Task5'

    ip = Column(CHAR(50), nullable=False)
