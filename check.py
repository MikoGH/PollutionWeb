import re
import datetime
from tables import *


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
    print(df['mpc'])
    return check_isNumber(df['mpc'])

# Проверка датасета Аварии
def check_incidents(df):
    return check_isDatetime(df['date'])

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
def check_emissioninventory(df):
    pass

# Проверка датасета Пользователи
def check_users(df):
    pass


# Вызывает соответствующую функцию проверки элементов модели
def check_model(new_df, model):
    if model == Substance:
        return check_substances(new_df)
    if model == Incident:
        return check_incidents(new_df)
    if model == Post:
        return check_posts(new_df)
    if model == EmissionInventory:
        return check_emissioninventory(new_df)
    if model == Measurement:
        return check_measurements(new_df)
    if model == Meteo:
        return check_meteo(new_df)
    return False