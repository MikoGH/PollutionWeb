from views_table import *
from processing import *
from flask import url_for
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory
from check import *


@app.route('/table/<string:table_name>/add', methods=['POST', 'GET'])
def add_choose_values(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]
    model = dct_models[table_name]
    headers = model.attr()
    headers_rus = model.attr_rus()
    posts = [elm[1] for elm in get_posts()]
    substances = [elm[1] for elm in get_substances()]

    return render_template("add.html", headers=headers, headers_rus=headers_rus, count_headers=len(headers), table_name=table_name, table_name_rus=table_name_rus, posts=posts, substances=substances, error='')

@app.route('/table/<string:table_name>/add_func', methods=['POST', 'GET'])
def add(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    headers = model.attr()
    headers_rus = model.attr_rus()
    posts = [elm[1] for elm in get_posts()]
    substances = [elm[1] for elm in get_substances()]

    # Новый датафрейм
    new_df = pd.DataFrame(columns=headers)
    new_df = new_df.drop('id', axis=1)

    # Установить соответствие столбцов
    line = []
    for header in headers:
        if header == 'id': continue
        line.append(request.form[f'{header}_value'])
    print(new_df.columns)
    new_df.loc[len(new_df)] = line

    if check_model(new_df, model):
        process_model(new_df, model)
    else:
        return render_template("add.html", headers=headers, headers_rus=headers_rus, count_headers=len(headers), table_name=table_name, table_name_rus=table_name_rus, posts=posts, substances=substances, error='Некорректный ввод')

    return redirect(url_for('table', table_name=table_name, page=1))