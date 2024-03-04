### Модули с предобработкой данных 

import pandas as pd
from datetime import datetime
import sqlite3
from sqlite3 import Error
import re


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
def read_table(table_name):
    query = f"""
    SELECT * FROM {table_name}
    """
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
        el['windDirection'] = re.findall('[\d,]+', el['windDirection'])
        if len(el['windDirection']) == 0:
            el['windDirection'] = None
        else:
            el['windDirection'] = el['windDirection'][0].replace(',','.')

        query = f'''
        INSERT INTO
        Measurements (idPost, date, windSpeed, windDirection, pressure, hydrogenSulfide)
        VALUES 
        ({idPost}, "{el['date']}", {el['windSpeed']}, {el['windDirection']}, {el['pressure']}, {el['hydrogenSulfide']});
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
        ("{el['date']}", {el['temperature']}, {el['pressure']}, {el['windSpeed']}, {el['windDirection']}, {el['humid']});
        '''
        execute_query(query) 
    return df

def process_substances(df):
    pass