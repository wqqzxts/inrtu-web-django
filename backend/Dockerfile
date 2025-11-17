FROM 3.12.12-slim

WORKDIR /app

RUN pip install poetry

COPY pyproject.toml poetry.lock* /app/

RUN poetry config virualenvs.create false
RUN poetry install --no-dev

COPY . /app

RUN poetry run python manage.py collectstatic --noinput

EXPOSE 8000

CMD ["uvicorn", "app.asgi:application", "--host", "0.0.0.0", "--port", "8000"]
