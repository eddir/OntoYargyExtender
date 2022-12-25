FROM python:3.9
LABEL maintainer="ea@rostkov.me"

RUN mkdir /app && mkdir /app/backend
RUN mkdir /app/backend/media
RUN mkdir /app/backend/seacare
RUN mkdir /app/backend/seacare/static
WORKDIR /app/backend

COPY ./backend/Pipfile /app/backend/
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until
RUN apt-get update
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --ignore-pipfile --deploy --skip-lock
RUN pip install django && pip install gunicorn && pip install kafka-python
# RUN python manage.py migrate django_celery_results
EXPOSE 8000