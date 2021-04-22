FROM python:3

RUN mkdir /site
COPY . /site/
WORKDIR /site

RUN pip install django==2.2.10
RUN pip install djangorestframework
RUN python3 manage.py makemigrations
RUN python3 manage.py migrate

ENTRYPOINT [ "python3", "manage.py" ]
CMD ["runserver", "0.0.0.0:8000"] 
