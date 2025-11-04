import json
import pandas as pd
from datetime import datetime as dt
from src import utils, views, services, reports

def run_all_features():
    """Запускает все реализованные функциональности и сохраняет результаты."""
    print("Загружаем транзакции...")
    df = utils.load_transactions()

    # 1. Главная страница (пример для текущей даты)
    print("Формируем главную страницу...")
    main_result = views.main_page(dt.now().strftime('%Y-%m-%d %H:%M:%S'))
    with open('output/main_page.json', 'w', encoding='utf-8') as f:
        json.dump(main_result, f, ensure_ascii=False, indent=2)

    # 2. Страница «События»
    print("Формируем страницу «События»...")
    events_result = views.events_page(df)
    with open('output/events_page.json', 'w', encoding='utf-8') as f:
        json.dump(events_result, f, ensure_ascii=False, indent=2)

    # 3. Сервисы
    print("Запускаем сервисы...")
    # Выгодные категории кешбэка (пример: май 2024)
    cashback = services.calculate_cashback_categories(
        df, 2024, 5
    )
    with open('output/cashback_categories.json', 'w', encoding='utf-8') as f:
        json.dump(cashback, f, ensure_ascii=False, indent=2)

    # Инвесткопилка (пример: май 2024, лимит 100)
    invest = services.investment_bank('2024-05', df, 100)
    with open('output/investment_bank.json', 'w', encoding='utf-8') as f:
        json.dump({"saved": invest}, f, ensure_ascii=False, indent=2)

    # Простой поиск (пример: поиск «кофе»)
    search = services.simple_search(df, 'кофе')
    with open('output/simple_search.json', 'w', encoding='utf-8') as f:
        json.dump(search, f, ensure_ascii=False, indent=2)

    # 4. Отчёты
    print("Формируем отчёты...")
    # Траты по категории (пример: «Кафе и рестораны»)
    spending_cat = reports.spending_by_category(
        df, 'Кафе и рестораны', dt.now().strftime('%Y-%m-%d')
    )

    # Траты по дням недели
    spending_weekday = reports.spending_by_weekday(
        df, dt.now().strftime('%Y-%m-%d')
    )

    # Траты в рабочий/выходной день
    spending_workday = reports.spending_by_workday(
        df, dt.now().strftime('%Y-%m-%d')
    )

    print("Готово! Результаты сохранены в папке output/")

if __name__ == "__main__":
    run_all_features()