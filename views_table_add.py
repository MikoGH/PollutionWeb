from views_table import *
from processing import *
from flask import url_for
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory

@app.route('/table/<string:table_name>/add', methods=['POST', 'GET'])
def upload_choose_values(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]

    return render_template("add.html", table_name=table_name, table_name_rus=table_name_rus, error="")

@app.route('/table/<string:table_name>/add_func', methods=['POST', 'GET'])
def add(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    headers = model.attr()

    # Новый датафрейм
    new_df = pd.DataFrame(columns=headers)
    # new_df.drop('id', axis=1)

    # Установить соответствие столбцов
    line = {}
    for header in headers:
        if header == 'id': continue
        line.update({header : request.form[f'{header}_file']})
    new_df = new_df.append(line, ignore_index = True)

    if model == Substance:
        process_substances(new_df)

    return redirect(url_for('table', table_name=table_name, page=1))