FROM python:3.12-slim

WORKDIR /app

COPY pyproject.toml poetry.lock* README.md ./

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --no-root

COPY . .

CMD ["bash"]
