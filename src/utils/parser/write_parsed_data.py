import json


async def write_data_to_json(data: dict, path: str) -> None:
    """
    Функция записывает распарсенные данные в json-файл
    :param data: словарь с данными
    :param path: директория и файл для записи
    :return: None
    """
    write_path = ''.join([path, 'Menu.json'])

    with open(write_path, 'w') as file:
        json.dump(data, file, ensure_ascii=False)
