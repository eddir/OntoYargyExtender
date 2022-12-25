FROM python:3

RUN mkdir /app
WORKDIR /app

# dont write pyc files
ENV PYTHONDONTWRITEBYTECODE 1
# dont buffer to stdout/stderr
ENV PYTHONUNBUFFERED 1

COPY ./ontologyExtender/Pipfile /app/

RUN apt-get update
RUN pip install --upgrade pip
RUN pip install pipenv && pipenv install --ignore-pipfile --deploy --skip-lock

CMD ["pipenv", "run", "python", "main.py"]