def filter_by_state (dictionaries:list, meaning: str='EXECUTED') -> list:
    """Фильтрует список словарей по значению ключа 'state'"""

    # Создаем новый список для хранения отфильтрованных результато
    filtered_list = []

    # Проходим по каждому словарю в списке
    for dictionary in dictionaries:
        if dictionary['state'] == meaning:
            filtered_list.append(dictionary)

    return filtered_list


def sort_by_date (dictionaries:list, state:bool=True) -> list:
    """Сортирует список словарей по дате"""
    if state == True:
        sorted_list = sorted(dictionaries, key=lambda x: x['date'], reverse=state) #Сортируем по убыванию если значение state = True
    else:
        sorted_list = sorted(dictionaries, key=lambda x: x['date']) #По возрастанию если значение False

    return sorted_list

