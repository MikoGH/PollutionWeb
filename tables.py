from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from wsgi import db
import bcrypt


class Substance(db.Model):
    __tablename__ = 'Substances'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    formula = db.Column(db.Text(), nullable=False)
    mpc = db.Column(db.Double(), nullable=False)

    def attr():
        return ['id', 'name', 'formula', 'mpc']
    def attr_rus():
        return ['id', 'вещество', 'формула', 'ПДК']
    

class Factory(db.Model):
    __tablename__ = 'Factories'
    id = db.Column(db.Integer(), primary_key=True)
    address = db.Column(db.Text(), nullable=False)
    type = db.Column(db.Text(), nullable=False)

    def attr():
        return ['id', 'address', 'type']
    def attr_rus():
        return ['id', 'адрес', 'тип']
    

class Post(db.Model):
    __tablename__ = 'Posts'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=False)
    coordinates = db.Column(db.Text(), nullable=False)
    height = db.Column(db.Float(), nullable=False)

    def attr():
        return ['id', 'name', 'coordinates', 'height']
    def attr_rus():
        return ['id', 'пост', 'координаты', 'высота']
    

class Incident(db.Model):
    __tablename__ = 'Incidents'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    idSubstance = db.Column(db.Integer(), nullable=False)
    idPost = db.Column(db.Integer(), nullable=False)

    def attr():
        return ['id', 'date', 'idSubstance', 'idPost']
    def attr_rus():
        return ['id', 'дата', 'вещество', 'пост']
    

class Map(db.Model):
    __tablename__ = 'Maps'
    id = db.Column(db.Integer(), primary_key=True)
    imagePath = db.Column(db.Text(), nullable=False)
    coordinates = db.Column(db.Text(), nullable=False)

    def attr():
        return ['id', 'imagePath', 'coordinates']
    def attr_rus():
        return ['id', 'путь', 'координаты']
    

class Meteo(db.Model):
    __tablename__ = 'Meteo'
    id = db.Column(db.Integer(), primary_key=True)
    date = db.Column(db.DateTime(), nullable=False)
    temperature = db.Column(db.Float(), nullable=False)
    pressure = db.Column(db.Float(), nullable=False)
    windSpeed = db.Column(db.Integer(), nullable=False)
    windDirection = db.Column(db.Integer(), nullable=False)
    humid = db.Column(db.Integer(), nullable=False)

    def attr():
        return ['id', 'date', 'temperature', 'pressure', 'windSpeed', 'windDirection', 'humid']
    def attr_rus():
        return ['id', 'дата', 'температура', 'давление', 'скорость ветра', 'направление ветра', 'влажность']


class EmissionInventory(db.Model):
    __tablename__ = 'EmissionInventory'
    id = db.Column(db.Integer(), primary_key=True)
    number = db.Column(db.Integer(), nullable=False)
    type = db.Column(db.Text(), nullable=False)
    height = db.Column(db.Float(), nullable=False)
    diameter = db.Column(db.Integer(), nullable=False)
    valueAFR = db.Column(db.Float(), nullable=False)
    speedAFR = db.Column(db.Float(), nullable=False)
    temperatureAFR = db.Column(db.Integer(), nullable=False)
    concentration = db.Column(db.Float(), nullable=False)
    annualEmission = db.Column(db.Float(), nullable=False)
    coordinates = db.Column(db.Text(), nullable=False)

    def attr():
        return ['id', 'number', 'type', 'height', 'width', 'diameter', 'valueAFR', 'speedAFR', 'temperatureAFR', 'concentration', 'annualEmission', 'coordinates']
    def attr_rus():
        return ['id', 'номер', 'тип', 'высота источника', 'ширина', 'диаметр', 'объём ГВС', 'скорость выхода ГВС', 'температура ГВС', 'концентрация', 'суммарные годовые выбросы', 'координаты']

class Measurement(db.Model):
    __tablename__ = 'Measurements'
    id = db.Column(db.Integer(), primary_key=True)
    idPost = db.Column(db.Integer(), nullable=False)
    date = db.Column(db.DateTime(), nullable=False)
    windSpeed = db.Column(db.Float(), nullable=False)
    windDirection = db.Column(db.Float(), nullable=False)
    pressure = db.Column(db.Float(), nullable=False)
    hydrogenSulfide = db.Column(db.Float(), nullable=False)

    def attr():
        return ['id', 'idPost', 'date', 'windSpeed', 'windDirection', 'pressure', 'hydrogenSulfide']
    def attr_rus():
        return ['id', 'пост', 'дата', 'скорость ветра', 'направление ветра', 'давление', 'концентрация сероводорода']
    

class User(db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.Text(), nullable=True)
    email = db.Column(db.Text(), nullable=False)
    password = db.Column(db.Text(), nullable=False)

    def attr():
        return ['id', 'name', 'email', 'password']
    def attr_rus():
        return ['id', 'имя', 'почта', 'пароль']
    
    def __init__(self, name, email, password):
        self.name=name
        self.email=email
        self.password=bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    def check_password(self, password):
        return bcrypt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))

