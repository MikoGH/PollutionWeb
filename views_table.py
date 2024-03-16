from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
from wsgi import app, db
from processing import *
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory

dct_models = {
    'Substances' : Substance,
    'Incidents' : Incident,
    'Measurements' : Measurement,
    'Meteo' : Meteo,
    'Posts' : Post,
    'Maps' : Map,
    'EmissionInventory' : EmissionInventory
}

dct_models_rus = {
    'Substances' : 'Вредные вещества',
    'Incidents' : 'Аварии',
    'Measurements' : 'Измерения',
    'Meteo' : 'Метео',
    'Posts' : 'Посты контроля',
    'Maps' : 'Карты',
    'EmissionInventory' : 'ИЗАВ'
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

    # Pagination
    per_page = 500
    pages=(model.query.count()+per_page-1)//per_page
    current_page = page
    if current_page > pages:
        current_page = 1
    table = model.query.paginate(page=current_page, per_page=per_page)

    # Posts
    posts = get_posts()
    dct_posts = {}
    for post in posts:
        dct_posts.update({post[0] : post[1]})
    # Substances
    substances = get_substances()
    dct_substances = {}
    for substance in substances:
        dct_substances.update({substance[0] : substance[1]})
    
    if len(table.items) == 0:
        error_text = 'Нет данных в таблице'
        headers = []
        headers_rus = []
    else:
        error_text = ''
        headers = model.attr()
        headers_rus = model.attr_rus()
    return render_template("table.html", pages=pages, current_page = current_page, headers=headers, headers_rus=headers_rus, table_data=table, table_name=table_name, table_name_rus=table_name_rus, dct_posts=dct_posts, dct_substances=dct_substances, error=error_text)
