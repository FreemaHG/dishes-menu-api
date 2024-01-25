FROM python:3.10-slim

COPY requirements/base.txt /src/requirements/base.txt

RUN pip install --no-cache-dir --upgrade -r /src/requirements/base.txt

COPY ./migrations /migrations

COPY alembic.ini /alembic.ini

COPY ./src /src

COPY ./docker /docker

# Разрешаем Docker выполнять команды в ./docker/<file>.sh (bash-команды),
# используемые для загрузки демонстрационных данных и запуска сервера
RUN chmod a+x docker/*.sh