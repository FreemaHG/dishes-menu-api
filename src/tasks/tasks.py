import asyncio

from celery import Celery

from src.config import RABBITMQ_HOST, RABBITMQ_PASS, RABBITMQ_USER
from src.services.synchronization.synchronization_menu import DataSynchronizationService

celery = Celery('tasks', broker=f'amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:5672')


@celery.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    """
    Добавляем периодические задачи
    """
    sender.add_periodic_task(15.0, synchronization_menu.s(), name='synchronization menu every 15 sec')


@celery.task
def synchronization_menu():
    """
    Синхронизация меню, подменю и блюд в БД согласно exel-файлу в src/admin/Menu.xlsx
    """
    loop = asyncio.get_event_loop()

    loop.run_until_complete(
        DataSynchronizationService.synchronization_db()
    )

# Запуск планировщика задач, который будет периодически посылать задачу воркеру
# celery -A src.tasks.tasks beat --loglevel=INFO

# Запуск воркета, который будет непосредственно выполнять задачу
# celery -A src.tasks.tasks worker --loglevel=INFO
