import os
from typing import Literal

from loguru import logger
from pydantic import ValidationError

from src.repositories.synchronization.last_change_time import LastChangeFileRepository
from src.schemas.parser.menu import MenusListParserSchema
from src.utils.parser.exel_parsing import ParseExel


class CheckDataService:
    """
    Сервис для проверки файла и данных перед началом синхронизации
    """

    @classmethod
    async def _availability(cls, file: str) -> bool:
        """
        Метод проверяет файл на наличие
        :param file: директория с файлом
        :return: True, если файл существует, иначе False
        """
        return os.path.isfile(file)

    @classmethod
    async def _get_change_time(cls, file: str) -> int:
        """
        Метод возвращает timestamp-время последнего изменения файла
        :param file: проверяемый файл
        :return: True, если файл существует, иначе False
        """
        return int(round(os.path.getmtime(file)))

    @classmethod
    async def _comparison_time_change(cls, file_time: int, last_time: int) -> bool:
        """
        Метод проверяет время изменения файла и сравнивает его с последним записанным
        :param file_time: время изменения файла
        :param last_time: последнее записанное время синхронизации
        :return: True, если файл новее последней записи
        """
        return bool(file_time and file_time <= last_time)

    @classmethod
    async def _get_parsed_data(cls, file: str) -> dict:
        """
        Метод возвращает распарсенные данные из файла
        :param file: файл с данными
        :return: словарь с распарсенными данными
        """
        return ParseExel.parse_data(file=file)

    @classmethod
    async def _data_validation(cls, data: dict) -> bool:
        """
        Метод проверяет данные на соответствие структуры при помощи схемы
        :param data: словарь с данными
        :return: True, если данные валидны, иначе False
        """
        try:
            MenusListParserSchema.validate(data)
            return True

        except ValidationError as e:
            logger.error(f'Невалидные данные: {e}')
            return False

    @classmethod
    async def check_file(cls, file: str) -> dict | Literal[False]:
        """
        Метод проверяет файл и данные перед синхронизацией с БД
        :param path: файл с данными
        :return: True, если все в порядке и можно синхронизировать, иначе False
        """

        if not await cls._availability(file=file):
            logger.warning(f'Отсутствует файл для синхронизации: {file}')
            return False

        time_change_file = await cls._get_change_time(file=file)
        last_change_time = await LastChangeFileRepository.get()

        if last_change_time:
            if await cls._comparison_time_change(file_time=time_change_file, last_time=last_change_time):
                logger.debug('Время изменения файла совпадает, обновление БД не требуется')
                return False

        data = await cls._get_parsed_data(file=file)

        if not await cls._data_validation(data=data):
            return False

        # Записываем в словарь время последнего изменения файла для последующей записи при синхронизации
        data['time_change_file'] = time_change_file

        return data
