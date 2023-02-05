from typing import Any
from logs.loggers import func_logger


@func_logger
def value_from_dict(multidict: dict, keys: list) -> Any:
    """
    Применяет метод get ко вложенным словарям по ключам
    :param multidict: словарь со вложенными словарями
    :param keys: список ключей
    :return: значение по ключам
    """
    value = multidict
    for key in keys:
        value = value.get(key)
        if value is None:
            break
    return value
