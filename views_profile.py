from flask import Flask, render_template, request, redirect, session
from flask_sqlalchemy import SQLAlchemy
# from flask_login import UserMixin
# from flask_wtf import wtforms, FlaskForm
# from wtforms import StringField, PasswordField, SubmitField, EmailField
# from wtforms.validators import InputRequired, Length, ValidationError
from wsgi import app, db
from tables import User


@app.route('/profile')
def profile():
    if not('name' in session):
        return redirect('/auth')
    else:
        return render_template("profile.html", name=session['name'])

@app.route('/auth', methods=['GET', 'POST'])
def auth():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user and user.check_password(password):
            session['name'] = user.name
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/profile')
        elif user and not(user.check_password(password)):
            return render_template('profile_auth.html', error='Неверный пароль')
        else:
            return render_template('profile_auth.html', error='Пользователь не существует')
    return render_template("profile_auth.html")

@app.route('/logout', methods=['GET', 'POST'])
def logout():
    session.pop('name', None)
    session.pop('email', None)
    session.pop('password', None)
    return redirect('/auth')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        password = request.form['password']
        user = User.query.filter_by(email=email).first()
        if user:
            return render_template("profile_register.html", error='Пользователь с указанным адресом электронной почты уже существует')
        new_user = User(name=name, email=email, password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('/profile')
    return render_template("profile_register.html")