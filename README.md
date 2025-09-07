# Проект ProjectSkyPro
## Описание 
Проект который в бэкенде будет готовить данные для отображения в новом виджете.
## Установка
1. Клонируйте репозиторий:
```
git clone https://github.com/RembotNiyaz/ProjectSkyPro.git
```
2. Установите зависимости:
```
pip install -r requirements.txt
```
## Использование 
```
# Маскировка карты
card_number = "1234567890123456"
print(get_mask_card_number(card_number))  # Вывод: 1234 56** **** 3456

# Маскировка счета
account_number = "40817810000000000000"
print(get_mask_account(account_number))  # Вывод: **0000

# Автоматическое определение
input_str = "Карта 1234567890123456"
print(mask_account_card(input_str))  # Вывод: Карта 1234 56** **** 3456

# Фильтрация данных
data = [
    {"state": "EXECUTED", "date": "2023-01-01"},
    {"state": "PENDING", "date": "2023-01-02"}
]
filtered_data = filter_by_state(data)

# Сортировка
sorted_data = sort_by_date(data, state=False)

# Преобразование даты
date_str = "2023-07-11T02:26:18.671407"
formatted_date = get_date(date_str)  # Вывод: 11.07.2023
```

## Лицензия:
Этот проект лицензирован по [лицензии MIT](LICENSE)
