from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
from wsgi import app, db
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory

dct_models = {
    'Substances' : Substance,
    'Incidents' : Incident,
    'Measurements' : Measurement,
    'Meteo' : Meteo,
    'Posts' : Post,
    'Maps' : Map,
    'EmissionInventories' : EmissionInventory
}

dct_models_rus = {
    'Substances' : 'Вредные вещества',
    'Incidents' : 'Аварии',
    'Measurements' : 'Измерения',
    'Meteo' : 'Метео',
    'Posts' : 'Посты контроля',
    'Maps' : 'Карты',
    'EmissionInventories' : 'ИЗАВ'
}

@app.route('/table/<string:table_name>/<int:page>', methods=['POST', 'GET'])
def table(table_name, page):
    if not('name' in session):
        return render_template("table_unavailable.html")

    if not(table_name in dct_models.keys()):
        table_name = 'Substances'
    new_table_name = str(request.form.get('select_table'))
    if new_table_name != 'None':
        table_name = new_table_name
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    table_name_rus = dct_models_rus[table_name]
    # table = model.query.all()

    per_page = 500
    pages=(model.query.count()+per_page-1)//per_page
    current_page = page
    if current_page > pages:
        current_page = 1
    table = model.query.paginate(page=current_page, per_page=per_page)
    if len(table.items) == 0:
        error_text = 'Нет данных в таблице'
        headers = []
    else:
        error_text = ''
        headers = model.attr()
    return render_template("table.html", pages=pages, current_page = current_page, headers=headers, table_data=table, table_name=table_name, table_name_rus=table_name_rus, error=error_text)

