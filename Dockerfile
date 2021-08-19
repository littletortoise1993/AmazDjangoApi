FROM python:3.7
RUN mkdir /usr/src/myapp -p
COPY . /usr/src/myapp
WORKDIR /usr/src/myapp
RUN pip install -r requirements.txt -i  https://mirrors.aliyun.com/pypi/simple/
WORKDIR /usr/src/myapp
CMD python manage.py runserver 0:8000
