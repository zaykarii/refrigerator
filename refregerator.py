from decimal import Decimal
from datetime import date, datetime, timedelta

# Объявление словаря goods с корректными датами
goods = {
    'Пельмени Универсальные': [
        {'amount': Decimal('0.5'), 'expiration_date': date(2023, 7, 15)},
        {'amount': Decimal('2'), 'expiration_date': date(2023, 8, 1)},
    ],
    'Вода': [
        {'amount': Decimal('1.5'), 'expiration_date': None}  # Обработка None
    ],
    'Молоко': [
        {'amount': Decimal('2'), 'expiration_date': date(2024, 12, 10)},
        {'amount': Decimal('1'), 'expiration_date': date(2024, 12, 5)}
    ],
    'Хлеб': [
        {'amount': Decimal('1'), 'expiration_date': date(2024, 12, 1)}
    ]
}

def add(goods, title, amount, expiration_date=None):
    if title in goods:
        goods[title].append({"amount": amount, "expiration_date": expiration_date})
    else:
        goods[title] = [{"amount": amount, "expiration_date": expiration_date}]

    return f"Продукт '{title}' добавлен."

def add_by_note(goods, note):
    parts = note.split()

    # Проверяем, что строка содержит хотя бы 3 части (название, количество, дата)
    if len(parts) < 3:
        print("Ошибка: строка должна содержать название, количество и срок годности.")
        return

    # Проверяем, является ли предпоследняя часть числом (количество)
    amount_part = parts[-2]
    if not amount_part.replace('.', '', 1).isdigit():
        print("Ошибка: количество должно быть числом.")
        return

    # Преобразуем количество в Decimal
    amount_of_goods = Decimal(amount_part)

    # Проверяем, является ли последняя часть даты в формате ГГГГ-ММ-ДД
    date_parts = parts[-1].split('-')
    if len(date_parts) != 3 or not all(part.isdigit() for part in date_parts):
        print("Ошибка: последняя часть строки не является датой в формате ГГГГ-ММ-ДД.")
        return

    # Преобразуем дату в формат date
    expiration_date = datetime.strptime(parts[-1], '%Y-%m-%d').date()

    # Объединяем все части строки, кроме последних двух, для названия продукта
    title = " ".join(parts[:-2])

    # Вызов функции add() для добавления нового продукта
    add(goods, title, amount_of_goods, expiration_date)

def find(goods, needle):
    results = []

    for key in goods:
        if needle.lower() in key.lower():
            results.append(key)

    return results

def amount(goods, needle):
    found_items = find(goods, needle)
    total_amount = {}

    for item in found_items:
        # Суммируем количество всех партий для каждого найденного товара
        total_amount[item] = sum(entry["amount"] for entry in goods[item])

    return total_amount

def expire(goods, in_advance_days=0):
    # Получаем текущую дату
    current_date = date.today()
    # Вычисляем дату, до которой нужно проверять срок годности
    expiry_date_limit = current_date + timedelta(days=in_advance_days)

    # Словарь для хранения продуктов и их партий, срок годности которых истекает
    expiring_items = {}

    # Перебираем все продукты и их партии
    for title, batches in goods.items():
        for batch in batches:
            # Проверяем, не равна ли дата срока годности None
            if batch["expiration_date"] is not None:
                expiration_date = batch["expiration_date"]

                # Проверяем, истекает ли срок годности партии
                if expiration_date <= expiry_date_limit:
                    if title not in expiring_items:
                        expiring_items[title] = []
                    expiring_items[title].append(batch)

    return expiring_items


# Тест для добавления нового продукта
add_by_note(goods, "Вода 2.5 2024-12-15")
print(goods)

# Тест для поиска количества товаров
print(amount(goods, "молоко"))

# Тест для проверки истекающих продуктов
print(expire(goods, 7))

# Тест для добавления нового продукта и проверки словаря
add_by_note(goods, "Сок 3 2024-12-20")
print(goods)  # Ожидается, что новый продукт "Сок" будет добавлен

# Тест для поиска количества товаров по имени
print(amount(goods, "Вода"))  # Должно вернуть сумму всех количеств воды

# Тест для проверки истекающих продуктов с разными значениями in_advance_days
print(expire(goods, 7))  # Проверка на продукты, срок годности которых истекает в течение 7 дней
print(expire(goods, 30))  # Проверка на продукты, срок годности которых истекает в течение 30 дней
