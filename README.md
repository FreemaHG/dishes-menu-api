# API для меню ресторана

Проект представляет собой API по работе с меню ресторана, все CRUD операции. Написан на фреймворке FastAPI
с использованием PostgreSQL в качестве основной БД и Redis для кэширования.
Для автоматической синхронизации БД с exel-файлом с меню используется планировщик Celery и брокер RabbitMQ.

## Оглавление
1. [Описание](#Описание)
2. [Инструменты](#Инструменты)
3. [Сборка](#Сборка)
   1. [Production](#Prod)
   2. [Тестирование](#Test)
   3. [Разработка](#Dev)
      1. [Запуск тестов](#Тестирование)
      2. [Планировщик задач Celery](#Celery)
      3. [Pre-commit хуки](#Pre-commit)
4. [Postman-тесты](#Postman-тесты)

## Описание

Даны 3 сущности: Меню, Подменю, Блюдо.

**Зависимости**:
* У меню есть подменю, которые к ней привязаны.
* У подменю есть блюда.

**Условия**:
* Блюдо не может быть привязано напрямую к меню, минуя подменю.
* Блюдо не может находиться в 2-х подменю одновременно.
* Подменю не может находиться в 2-х меню одновременно.
* Если удалить меню, должны удалиться все подменю и блюда этого меню.
* Если удалить подменю, должны удалиться все блюда этого подменю.
* Цены блюд выводить с округлением до 2 знаков после запятой.
* Во время выдачи списка меню, для каждого меню добавлять кол-во подменю и блюд в этом меню.
* Во время выдачи списка подменю, для каждого подменю добавлять кол-во блюд в этом подменю.

При помощи планировщика задач Celery каждые 15 секунд идет проверка локального exel-файла (src/admin/Menu.xlsx)
на изменения. При наличии изменений БД автоматически синхронизируется с файлом.

## Инструменты
* **Python** (3.10);
* **FastAPI** (asynchronous Web Framework);
* **PostgreSQL** (database);
* **SQLAlchemy** (working with database from Python);
* **Alembic** (database migrations made easy);
* **Pydantic** (data verification);
* **Redis** (caching);
* **Celery** (database synchronization);
* **RabbitMQ** (message broker for celery);
* **Pytest** (tests);
* **Docker Compose**.

## Сборка

1. Скачиваем содержимое репозитория в отдельную папку:
    ```
    git clone https://github.com/FreemaHG/dishesApiProject.git
    ```

### Prod

2. Переименовываем файл "**.env.prod.template**" в "**.env**".


3. Собираем и запускаем контейнеры:
   ```
   docker-compose up -d
   ```

   После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    http://127.0.0.1:8000/docs/
    ```

4. Остановка и удаление контейнеров:
   ```
   docker-compose down
   ```

### Test

2. Переименовываем файл "**.env.test.template**" в "**.env**".


3. Запускаем контейнеры с тестовыми БД и Redis:
   ```
   docker-compose -f docker-compose-tests.yml up -d test_postgres test_cache
   ```

4. Запускаем контейнер с тестами:

   ```
   docker-compose -f docker-compose-tests.yml up test_api
   ```

   **Примечание**: в приложении реализована функция аналог reverse() в Django,
которая используется при тестировании роутов.


5. Удаление контейнеров:
   ```
   docker-compose -f docker-compose-tests.yml down
   ```

### Dev

2. Переименовываем файл "**.env.dev.template**" в "**.env**", при необходимости можно задать свои параметры.


3. Создаем и активируем виртуальное окружение:
   ```
   python3.10 -m venv venv
   ```
   ```
   source venc/bin/activate
   ```

   **ВАЖНО**: для корректной работы пакета fastapi_redis необходим python **версии 3.10**!


4. Устанавливаем зависимости:
   ```
   pip install -r requirements/dev.txt
   ```

5. Собираем и запускаем контейнер с PostgreSQL:
   ```
   docker-compose up -d postgres
   ```

6. Применяем миграции (создаем структуру БД):
   ```
   alembic upgrade head
   ```

7. Очищаем Redis (на всякий случай от остаточных данных):
   ```
   redis-cli flushall
   ```

8. Запускаем сервер:
   ```
   uvicorn src.main:app --reload
   ```

9. Остановка и удаление контейнера с PostgreSQL:
   ```
   docker-compose down postgres
   ```

#### Тестирование

1. Перед стартом тестов запускаем контейнер с тестовой БД:
   ```
   docker-compose -f docker-compose-tests.yml up -d test_postgres
   ```

2. Запуск тестов:
   ```
   pytest -v
   ```

2. Удаление контейнера с тестовой БД:
   ```
   docker-compose -f docker-compose-tests.yml down test_postgres
   ```

#### Celery

1. Запускаем контейнер с RabbitMQ:
   ```
   docker-compose up -d rabbitmq
   ```

2. Запускаем воркер Celery:
   ```
   celery -A src.tasks.tasks worker --loglevel=INFO
   ```

3. В новом окне терминала запускаем планировщик задач Celery:
   ```
   celery -A src.tasks.tasks beat --loglevel=INFO
   ```

   Планировщик каждые 15 секунд проверяет файл scr/admin/Menu.xlsx и синхронизирует данные с БД в случае изменений.


   **ВАЖНО**: не забываем запустить контейнер с PostgreSQL и выполнить миграции (создать структуру БД)!

#### Pre-commit

В проекте используются Git-хуки для автоматической проверки и форматирования кода перед созданием коммита.

**ВАЖНО**: на локальной машине разработчика должен быть установлен пакет **pre-commit**

Применяемые хуки описаны в корне проекта в файле .pre-commit-config.yaml

Для активации хуков вводим:
   ```
   pre-commit install
   ```
Предварительная проверка и форматирование кода:
   ```
   pre-commit run --all-files
   ```

## Postman-тесты

1. Запускаем приложение в режиме Dev либо Prod (см. шаги выше).

**ВАЖНО**: Во время запуска тестового сценария БД должна быть **пуста**!

В postman в левом верхнем углу нажимаем "import":
![](/postman/1.png)

Перетаскиваем во всплывшее окно два файла (коллекция тестов и переменные окружения) из папки postman
в корне проекта. Подтверждаем импорт:
![](/postman/2.png)

Либо слева во вкладке "Environments" кликаем галочку рядом с переменными окружения.
Либо справа сверху в выпадающем списке выбираем загруженные переменные окружения.
![](/postman/3.png)

Далее кликаем: слева во вкладке "Collections" -> три точки на папке "Тестовый сценарий" -> "Run folder"
![](/postman/4.png)

Для запусков тестов нажимаем "Run Menu app"
![](/postman/5.png)

Радуемся успешно пройденным тестам.
![](/postman/6.png)
