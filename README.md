# Описание проекта

Проект представляет собой API по работе с меню ресторана, все CRUD операции. Написан на фреймворке FastAPI 
с использованием PostgreSQL в качестве БД. Для проверки API предусмотрена Postman-коллекция с тестами. 

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

## Используемые инструменты:
* **Python** (3.11);
* **FastAPI** (asynchronous Web Framework);
* **PostgreSQL** (database);
* **SQLAlchemy** (working with database from Python);
* **Alembic** (database migrations made easy);
* **Pydantic** (data verification);
* **Docker Compose** (for run the DB).

## Сборка и запуск
1. Скачиваем содержимое репозитория в отдельную папку:
    ```
    git clone https://github.com/FreemaHG/dishesApiProject.git
    ```
2. Переименовываем файл "**.env.template**" в "**.env**", при необходимости можно задать свои параметры.


3. Собираем и запускаем контейнеры с API и БД:
   ```
   docker-compose up -d
   ```

После сборки и запуска приложения ознакомиться с документацией API можно по адресу:
    ```
    http://127.0.0.1:8000/docs/
    ```

## Запуск тестов



## Запуск тестов в Postman

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

Радуемся успешно пройденным тестам
![](/postman/6.png)