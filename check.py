import re
import datetime

# Проверка на число
def check_isNumber(values):
    for value in values:
        if value.count('.') == 1:
            value = value.replace('.', '')
        elif value.count(',') == 1:
            value = value.replace(',', '')

        if not(value.isdigit()): return False
    return True

# Проверка на дату
def check_isDatetime(values):
    for value in values:
        try:
            if '.' in value:
                datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
            elif '-' in value:
                datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
            else: 
                return False
        except:
            return False
    return True

# Проверка датасета Вредные вещества
def check_substances(df):
    return check_isNumber(df['mpc'])

# Проверка датасета Аварии
def check_incidents(df):
    pass

# Проверка датасета Посты контроля
def check_posts(df):
    pass

# Проверка датасета Измерения
def check_measurements(df):
    pass

# Проверка датасета Метео параметры
def check_meteo(df):
    pass

# Проверка датасета ИЗАВ
def check_emissioninventories(df):
    pass

# Проверка датасета Пользователи
def check_users(df):
    pass