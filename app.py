from flask import Flask, render_template, session
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
db = SQLAlchemy(app)
app.config['SECRET_KEY'] = 'secret_key'

from views import *

if __name__ == "__main__":
    app.run(debug=True)
    