FROM python:3.9-alpine

WORKDIR /app
COPY . /app

RUN poetry install

ENV DJANGO_SETTINGS_MODULE=mamamia.settings
EXPOSE 8000

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]