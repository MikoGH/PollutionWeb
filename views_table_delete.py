from views_table import *
from processing import *
from flask import url_for
from tables import Substance, Incident, Measurement, Meteo, Factory, Post, Map, EmissionInventory


@app.route('/table/<string:table_name>/delete/<int:id>', methods=['POST', 'GET'])
def delete(table_name, id):
    delete_from_table(table_name, id)
    return redirect(url_for('table', table_name=table_name, page=1))
