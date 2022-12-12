FROM python:3.8
RUN python -m pip install flask sqlalchemy pymysql
COPY . /mock
WORKDIR /mock
EXPOSE 9000
CMD python mock.py
