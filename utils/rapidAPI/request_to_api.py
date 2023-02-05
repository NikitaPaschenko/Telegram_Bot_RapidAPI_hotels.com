from typing import Optional, Dict
import requests
from loguru import logger
from logs.loggers import func_logger


@func_logger
def request_to_api(method: str, url: str, headers: Dict[str, str],
                   **kwargs) -> Optional[str]:
    """
    Выполняет запрос к API
    :param method: метод для запроса
    :param url: адрес для запроса
    :param headers: параметры доступа
    :param kwargs: прочие параметры
    :return: результат запроса или None
    """
    try:
        response = requests.request(method=method, url=url, headers=headers,
                                    timeout=10, **kwargs)
        if response.status_code == requests.codes.ok:
            return response.text
    except (requests.exceptions.Timeout, requests.exceptions.TooManyRedirects,
            requests.exceptions.RequestException) as exc:
        logger.error(str(exc))
        return None
