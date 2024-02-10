from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory

dct_models = {
    'Вредные вещества' : Substance,
    'Аварии' : Incident,
    'Измерения' : Measurement,
    'Метео' : Meteo,
    'Посты контроля' : Post,
    'Карты' : Map,
    'ИЗАВ' : EmissionInventory
}

@app.route('/table', methods=['POST', 'GET'])
def table():
    if not('name' in session):
        return render_template("table_unavailable.html")

    table_name = str(request.form.get('select_table'))
    if table_name == 'None':
        table_name = 'Вредные вещества'
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    table = model.query.all()
    error_text = 'Нет данных в таблице'
    headers = []
    if len(table) > 0:
        headers = table[0].attr()
        error_text = ''
    # print(headers)
    return render_template("table.html", headers=headers, tableData=table, tableName=table_name, error=error_text)

