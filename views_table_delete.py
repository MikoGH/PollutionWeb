from views_table import *
from processing import *
from flask import url_for
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory


@app.route('/table/<string:table_name>/delete', methods=['POST', 'GET'])
def delete_choose_id(table_name):
    if not('name' in session):
        return render_template("table_unavailable.html")
    
    table_name_rus = dct_models_rus[table_name]

    return render_template("delete.html", table_name=table_name, table_name_rus=table_name_rus, error='')


@app.route('/table/<string:table_name>/delete_func', methods=['POST', 'GET'])
def delete(table_name, id=''):
    table_name_rus = dct_models_rus[table_name]
    if id == '':
        from_id = request.form['from_id']
        to_id = request.form['to_id']
        if from_id.isdigit() and to_id.isdigit():
            for i in range(int(from_id), int(to_id)+1):
                delete_from_table(table_name, i)
        else:
            return render_template("delete.html", table_name=table_name, table_name_rus=table_name_rus, error='Некорректный ввод')
    else:
        delete_from_table(table_name, id)
    return redirect(url_for('table', table_name=table_name, page=1))
