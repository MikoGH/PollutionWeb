### Модули с предобработкой данных 

import pandas as pd
from datetime import datetime
import sqlite3
from sqlite3 import Error
import re
from tables import *


# Создать соединение с бд
def create_connection():
    connection = None
    try:
        connection = sqlite3.connect('./instance/data.db')
    except Error as e:
        print(f"The error '{e}' occurred")

    return connection


# Запрос на запись в бд
def execute_query(query):
    con = create_connection()
    cursor = con.cursor()
    try:
        cursor.execute(query)
        con.commit()
        con.close()
    except Error as e:
        print(f"The error '{e}' occurred")


# Запрос на чтение из бд
def execute_read_query(query):
    con = create_connection()
    cursor = con.cursor()
    result = None
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        con.close()
        return result
    except Error as e:
        print(f"The error '{e}' occurred")


# Считать и вернуть таблицу
def read_table(table_name, id=-1):
    if id == -1:
        query = f"""
        SELECT * FROM {table_name}
        """
    else:
        query = f"""
        SELECT * FROM {table_name}
        WHERE id = {id}
        """
    return execute_read_query(query) 



# Очистить таблицу
def clear_table(table_name):
    query = f"""
    DELETE FROM {table_name}
    """
    execute_query(query) 


def to_date_format(value):
    if '.' in value:
        return datetime.strptime(value, '%d.%m.%Y %H:%M:%S')
    if '-' in value:
        return datetime.strptime(value, '%Y-%m-%d %H:%M:%S')
    
def get_posts():
    query = f'''
    SELECT id, name FROM Posts
    '''
    return execute_read_query(query)

def get_substances():
    query = f'''
    SELECT id, name FROM Substances
    '''
    return execute_read_query(query)

# Обработка и запись датасета Измерения
def process_measurements(df):
    # clear_table('Measurements')
    for i, el in df.iterrows():
        query = f'''
        SELECT id, name FROM Posts
        WHERE name = "{el['idPost']}"
        LIMIT 1;
        '''
        idPost = execute_read_query(query)[0][0]
        el['windDirection'] = re.findall(r'[\d,]+', el['windDirection'])
        if len(el['windDirection']) == 0:
            el['windDirection'] = None
        else:
            el['windDirection'] = el['windDirection'][0].replace(',','.')

        query = f'''
        INSERT INTO
        Measurements (idPost, date, windSpeed, windDirection, pressure, hydrogenSulfide)
        VALUES 
        ({idPost}, "{to_date_format(el['date'])}", {el['windSpeed']}, {el['windDirection']}, {el['pressure']}, {el['hydrogenSulfide']});
        '''
        # execute_query(query) 
    return df

# Обработка и запись датасета метео параметров
def process_meteo(df):
    # обработка
    for i, el in df.iterrows():
        df['temperature'][i] = str(df['temperature'][i]).replace(',', '.')
    # запись
    for i, el in df.iterrows():
        query = f'''
        INSERT INTO
        Meteo (date, temperature, pressure, windSpeed, windDirection, humid)
        VALUES
        ("{to_date_format(el['date'])}", {el['temperature']}, {el['pressure']}, {el['windSpeed']}, {el['windDirection']}, {el['humid']});
        '''
        execute_query(query) 
    return df

# Обработка и запись датасета вредных веществ
def process_substances(df):
    # обработка
    for i, el in df.iterrows():
        df['mpc'][i] = str(df['mpc'][i]).replace(',', '.')
        if '/' in df['mpc'][i]:
            nums = df['mpc'][i].split('/')
            try:
                df['mpc'][i] = round(float(nums[0]) / float(nums[1]), 1)
            except:
                df['mpc'][i] = None
    # запись
    for i, el in df.iterrows():
        query = f'''
        INSERT INTO
        Substances (name, formula, mpc)
        VALUES
        ("{el['name']}", "{el['formula']}", {el['mpc']});
        '''
        execute_query(query) 
    return df

# Обработка и запись датасета ИЗАВ
def process_emissioninventory(df):
    # запись
    for i, el in df.iterrows():
        query = f'''
        INSERT INTO
        EmissionInventory (number, type, height, width, diameter, valueAFR, speedAFR, temperatureAFR, concentration, annualEmission, coordinates)
        VALUES
        ({el['number']}, "{el['type']}", {el['height']}, {el['width']}, {el['diameter']}, {el['valueAFR']}, {el['speedAFR']}, {el['temperatureAFR']}, {el['concentration']}, {el['annualEmission']}, "{el['coordinates']}");
        '''
        execute_query(query) 
    return df

# Обработка и запись датасета Посты
def process_posts(df):
    for i, el in df.iterrows():
        query = f'''
        INSERT INTO
        Posts (name, coordinates, height)
        VALUES
        ("{el['name']}", "{el['coordinates']}", {el['height']});
        '''
        execute_query(query) 
    return df

# Обработка и запись датасета Аварии
def process_incidents(df):
    for i, el in df.iterrows():
        query = f'''
        SELECT id, name FROM Posts
        WHERE name = "{el['idPost']}"
        LIMIT 1;
        '''
        idPost = execute_read_query(query)[0][0]
        query = f'''
        SELECT id, name FROM Substances
        WHERE name = "{el['idSubstance']}"
        LIMIT 1;
        '''
        idSubstance = execute_read_query(query)[0][0]
        query = f'''
        INSERT INTO
        Incidents (date, idPost, idSubstance)
        VALUES
        ("{to_date_format(el['date'])}", "{idPost}", {idSubstance});
        '''
        execute_query(query) 
    return df 

    
# def change_date_format():
#     query = f'''
#     SELECT id, date FROM Measurements
#     '''
#     df = execute_read_query(query)
#     for el in df:
#         if '-' in el[1]:
#             continue
#         date = to_date_format(el[1])
#         # print(el)
#         query = f'''
#         UPDATE Measurements
#         SET date = "{date}"
#         WHERE id = {el[0]};
#         '''
#         execute_query(query) 

# Изменение датасета вредных веществ
def edit_substances(df):
    # обработка
    for i, el in df.iterrows():
        df['mpc'][i] = str(df['mpc'][i]).replace(',', '.')
        if '/' in df['mpc'][i]:
            nums = df['mpc'][i].split('/')
            try:
                df['mpc'][i] = round(float(nums[0]) / float(nums[1]), 1)
            except:
                df['mpc'][i] = None
    # запись
    for i, el in df.iterrows():
        query = f'''
        UPDATE Substances 
        SET name="{el['name']}", formula="{el['formula']}", mpc={el['mpc']})
        WHERE id = {el['id']};
        '''
        execute_query(query) 
    return df

# Изменение датасета ИЗАВ
def edit_emissioninventory(df):
    # запись
    for i, el in df.iterrows():
        query = f'''
        UPDATE EmissionInventory 
        SET number={el['number']}, type="{el['type']}", height={el['height']}, width={el['width']}, diameter={el['diameter']}, valueAFR={el['valueAFR']}, speedAFR={el['speedAFR']}, temperatureAFR={el['temperatureAFR']}, concentration={el['concentration']}, annualEmission={el['annualEmission']}, coordinates="{el['coordinates']}"
        WHERE id = {el['id']};
        '''
        execute_query(query) 
    return df

# Изменение датасета Посты
def edit_posts(df):
    for i, el in df.iterrows():
        query = f'''
        UPDATE Posts 
        SET name = "{el['name']}", coordinates = "{el['coordinates']}", height ={el['height']}
        WHERE id = {el['id']};
        '''
        execute_query(query) 
    return df

# Изменение датасета Аварии
def edit_incidents(df):
    for i, el in df.iterrows():
        query = f'''
        SELECT id, name FROM Posts
        WHERE name = "{el['idPost']}"
        LIMIT 1;
        '''
        idPost = execute_read_query(query)[0][0]
        query = f'''
        SELECT id, name FROM Substances
        WHERE name = "{el['idSubstance']}"
        LIMIT 1;
        '''
        idSubstance = execute_read_query(query)[0][0]
        query = f'''
        UPDATE Incidents
        SET date = "{to_date_format(el['date'])}", idPost = {idPost}, idSubstance = {idSubstance}
        WHERE id = {el['id']};
        '''
        execute_query(query) 
    return df 


# Изменение датасета вредных веществ
def delete_from_table(table_name, id):
    query = f'''
    DELETE FROM {table_name} 
    WHERE id = {id};
    '''
    execute_query(query) 


# Вызывает соответствующую функцию добавления элементов модели
def process_model(new_df, model):
    if model == Substance:
        process_substances(new_df)
    if model == Incident:
        process_incidents(new_df)
    if model == Post:
        process_posts(new_df)
    if model == EmissionInventory:
        process_emissioninventory(new_df)
    if model == Measurement:
        process_measurements(new_df)
    if model == Meteo:
        process_meteo(new_df)


# Вызывает соответствующую функцию изменения элементов модели
def edit_model(new_df, model):
    if model == Substance:
        edit_substances(new_df)
    if model == Incident:
        edit_incidents(new_df)
    if model == Post:
        edit_posts(new_df)
    if model == EmissionInventory:
        edit_emissioninventory(new_df)