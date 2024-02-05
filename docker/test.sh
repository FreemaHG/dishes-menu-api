#!/bin/bash

# Очистка Redis
redis-cli flushall

# Запуск тестов
pytest -v
