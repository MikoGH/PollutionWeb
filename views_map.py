from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from wsgi import app, db
from tables import Substance


@app.route('/')
@app.route('/map')
def map():
    return render_template("map.html")

