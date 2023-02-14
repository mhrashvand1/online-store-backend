# pull official base image
FROM python:3.10-alpine

# set work directory
WORKDIR /usr/src/app

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install psycopg2 dependencies
RUN apk update \
    && apk add postgresql-dev gcc python3-dev musl-dev 

# install dependencies
RUN pip install --upgrade pip
RUN pip install Pillow
COPY ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY . .

CMD while ! python manage.py sqlflush > /dev/null 2>&1 ; do sleep 1; done && \
    while ! python manage.py test_redis > /dev/null 2>&1 ; do sleep 1; done && \
    python manage.py makemigrations --noinput && \
    python manage.py migrate --noinput && \
    # python manage.py collectstatic --noinput && \ 
    # gunicorn -b 0.0.0.0:8000 config.wsgi;
    python manage.py runserver 0.0.0.0:8000