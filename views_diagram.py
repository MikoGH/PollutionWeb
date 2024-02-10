from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy
from app import app, db
from tables import Substance

@app.route('/diagram')
def diagram():
    return render_template("diagram.html")

