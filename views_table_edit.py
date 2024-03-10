from views_table import *
from processing import *
from flask import url_for
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory


@app.route('/table/<string:table_name>/edit/<int:id>', methods=['POST', 'GET'])
def edit_choose_values(table_name, id):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]
    model = dct_models[table_name]
    headers = model.attr()
    headers_rus = model.attr_rus()
    
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

    # Считывание данных
    table = read_table(table_name, id=id)[0]
    dct_values = {}
    for i, header in enumerate(headers):
        dct_values.update({header : table[i]})

    return render_template("edit.html", dct_values=dct_values, headers=headers, headers_rus=headers_rus, count_headers=len(headers), table_name=table_name, table_name_rus=table_name_rus, dct_posts=dct_posts, dct_substances=dct_substances, error="")

@app.route('/table/<string:table_name>/edit_func/<int:id>', methods=['POST', 'GET'])
def edit(table_name, id):
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
        if header == 'id': 
            line.append(id)
        else:
            line.append(request.form[f'{header}_value'])
    new_df.loc[len(new_df)] = line
    print(new_df)

    if model == Substance:
        edit_substances(new_df)
    if model == Incident:
        edit_incidents(new_df)
    if model == Post:
        edit_posts(new_df)
    if model == EmissionInventory:
        edit_emissioninventory(new_df)

    return redirect(url_for('table', table_name=table_name, page=1))