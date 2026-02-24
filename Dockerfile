FROM python:3.12-slim

WORKDIR /app

RUN pip install --upgrade pip

COPY pyproject.toml ./

RUN pip install ".[all]" || pip install -r requirements.txt || echo "Using pyproject.toml dependencies"

COPY . .

RUN python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["gunicorn", "config.wsgi:application", "--bind", "0.0.0.0:8000"]