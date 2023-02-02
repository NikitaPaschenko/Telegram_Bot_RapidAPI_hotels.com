from datetime import date


def exit_date(data: str) -> date:
    """
    Функция, форматирующая дату в формат date из datetime
    :param data: Информация из календаря
    :return: Дата в формате date из datetime
    """
    lst_date = data.split(';')[1:]
    lst_date = [int(elem) for elem in lst_date]
    my_date = date(year=lst_date[0], month=lst_date[1], day=lst_date[2])
    return my_date
