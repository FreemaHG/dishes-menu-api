#!/bin/bash

# Если передан аргумент "celery"
if [[ "${1}" == "worker" ]]; then
  # Запуск планировщика задач, который будет периодически посылать задачу воркеру
  celery --app=src.tasks.tasks:celery worker -l INFO
elif [[ "${1}" == "beat" ]]; then
  # Запуск воркета, который будет непосредственно выполнять задачу
  celery --app=src.tasks.tasks:celery beat -l INFO
fi
