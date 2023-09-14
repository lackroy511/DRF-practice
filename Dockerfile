FROM python:3.11

WORKDIR /code

COPY pyproject.toml poetry.lock /code/

RUN pip install poetry && poetry config virtualenvs.create false && poetry install --no-root

COPY . /code/ 

ENV PATH="/code/.poetry/bin:$PATH"