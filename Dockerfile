FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip
RUN pip install .

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]