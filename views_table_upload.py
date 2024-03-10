from views_table import *
from processing import *
from flask import url_for

@app.route('/table/<string:table_name>/upload/choose_file', methods=['POST', 'GET'])
def upload_choose_file(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]

    return render_template("upload_choose_file.html", table_name=table_name, table_name_rus=table_name_rus, error="")

@app.route('/table/<string:table_name>/upload/set_columns', methods=['POST', 'GET'])
def upload_set_columns(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]

    if not('file' in request.files):
        return render_template("upload_choose_file.html", table_name=table_name, table_name_rus=table_name_rus, error="Файл не выбран")
    file = request.files['file']
    sheet = request.form['sheet']
    # if not(file.format)
    file.save('upload.xlsx')

    df = pd.read_excel('upload.xlsx', sheet_name=sheet)
    columns = df.columns
    
    table_name_rus = dct_models_rus[table_name]
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    headers = model.attr()
    headers_rus = model.attr_rus()

    return render_template("upload_set_columns.html", headers=headers, headers_rus=headers_rus, count_headers=len(headers), columns=columns, table_name=table_name, table_name_rus=table_name_rus, sheet=sheet, error="")

@app.route('/table/<string:table_name>/upload', methods=['POST', 'GET'])
def upload(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]
    sheet = request.args['sheet']
    
    # Чтение сохранённого датафрейма
    df = pd.read_excel('upload.xlsx', sheet_name=sheet)
    columns = df.columns
    
    model = dct_models[table_name]  # Модель таблицы в зависимости от выбранной пользователем таблицы
    headers = model.attr()
    headers_rus = model.attr_rus()

    # Новый датафрейм
    new_df = pd.DataFrame(columns=headers)
    new_df.drop('id', axis=1)

    # Установить соответствие столбцов
    for header in headers:
        if header == 'id': continue
        # Если одно из значений не выбрано
        if request.form[f'{header}_file'] == "": 
            return render_template("upload_set_columns.html", headers=headers, headers_rus=headers_rus, count_headers=len(headers), columns=columns, table_name=table_name, table_name_rus=table_name_rus, sheet=sheet, error="Не все соответствия установлены")

        new_df[header] = df[request.form[f'{header}_file']]
    process_meteo(new_df)

    return redirect(url_for('table', table_name=table_name, page=1))