import re
import datetime
from tables import *


# Проверка на число
def check_isNumber(values):
    for value in values:
        value = str(value)
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
    return check_isDatetime(df['date'])

# Проверка датасета Посты контроля
def check_posts(df):
    return check_isNumber(df['height'])

# Проверка датасета Измерения
def check_measurements(df):
    return check_isDatetime(df['date']) and check_isNumber(df['windSpeed']) and check_isNumber(df['windDirection']) and check_isNumber(df['pressure']) and check_isNumber(df['hydrogenSulfide'])

# Проверка датасета Метео параметры
def check_meteo(df):
    return check_isDatetime(df['date']) and check_isNumber(df['temperature']) and check_isNumber(df['pressure']) and check_isNumber(df['windSpeed']) and check_isNumber(df['windDirection'])  and check_isNumber(df['humid'])

# Проверка датасета ИЗАВ
def check_emissioninventory(df):
    return check_isNumber(df['number']) and check_isNumber(df['height']) and check_isNumber(df['width']) and check_isNumber(df['diameter']) and check_isNumber(df['valueAFR']) and check_isNumber(df['speedAFR']) and check_isNumber(df['temperatureAFR']) and check_isNumber(df['concentration']) and check_isNumber(df['annualEmission'])

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