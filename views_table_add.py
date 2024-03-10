from views_table import *
from processing import *
from flask import url_for
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory


@app.route('/table/<string:table_name>/add', methods=['POST', 'GET'])
def upload_choose_values(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]
    model = dct_models[table_name]
    headers = model.attr()
    headers_rus = model.attr_rus()
    posts = [elm[1] for elm in get_posts()]
    substances = [elm[1] for elm in get_substances()]

    return render_template("add.html", headers=headers, headers_rus=headers_rus, count_headers=len(headers), table_name=table_name, table_name_rus=table_name_rus, posts=posts, substances=substances, error="")

@app.route('/table/<string:table_name>/add_func', methods=['POST', 'GET'])
def add(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    headers = model.attr()

    # Проверка на корректность выбранных данных

    # Новый датафрейм
    new_df = pd.DataFrame(columns=headers)
    # new_df.drop('id', axis=1)

    # Установить соответствие столбцов
    line = []
    for header in headers:
        if header == 'id': continue
        # new_df.loc[header, -1] = request.form[f'{header}_value']
        # line.update({header : request.form[f'{header}_value']})
        line.append(request.form[f'{header}_value'])
    # new_df = new_df.append(line, ignore_index = True)
    # new_df = new_df.append(line)
    new_df.loc[len(new_df)] = line
    print(new_df)

    if model == Substance:
        process_substances(new_df)
    if model == Incident:
        process_incidents(new_df)
    if model == Post:
        process_posts(new_df)
    if model == EmissionInventory:
        process_emissioninventory(new_df)

    return redirect(url_for('table', table_name=table_name, page=1))