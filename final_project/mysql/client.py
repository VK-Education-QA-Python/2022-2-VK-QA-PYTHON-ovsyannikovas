import sqlalchemy
from sqlalchemy.orm import sessionmaker
from mysql.models import User


class MysqlClient:

    def __init__(self, db_name='vkeducation', user='test_qa', password='qa_test'):
        self.user = user
        self.port = '3306'
        self.password = password
        self.host = '127.0.0.1'
        self.db_name = db_name

        self.connection = None
        self.engine = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''
        url = f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        self.engine = sqlalchemy.create_engine(url)
        self.connection = self.engine.connect()
        session = sessionmaker(bind=self.connection.engine)
        self.session = session()

    def execute_query(self, query, fetch=False):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def add_user(self, name, surname, username, password, email, middle_name=None, access=1):
        test_user = User(
            name=name,
            surname=surname,
            username=username,
            password=password,
            email=email,
            access=access
        )
        self.session.add(test_user)
        self.session.commit()
        return test_user

    def delete_user(self, username):
        user = self.select_by_username(username)
        self.session.delete(user)
        self.session.commit()
        return user

    def select_by_username(self, username):
        self.session.commit()
        return self.session.query(User).filter(User.username == username).first()

    def select_by_email(self, email):
        self.session.commit()
        return self.session.query(User).filter(User.email == email).first()

    def is_user_exist(self, username):
        user = self.select_by_username(username)
        return True if user else False

    def get_access_by_username(self, username):
        try:
            user = self.select_by_username(username)
            return user.access
        except AttributeError:
            return None

    def get_password_by_username(self, username):
        try:
            user = self.select_by_username(username)
            return user.password
        except AttributeError:
            return None

    def get_email_by_username(self, username):
        try:
            user = self.select_by_username(username)
            return user.email
        except AttributeError:
            return None

    def get_username_by_email(self, email):
        try:
            user = self.select_by_email(email)
            return user.username
        except AttributeError:
            return None

    def block_by_username(self, username):
        user = self.select_by_username(username)
        user.access = 0
        self.session.commit()
