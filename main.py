from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, request, session
import time
# import requests
import json
from news_model import *
from db import *
from users_model import *

db = DB()
app = Flask(__name__)
app.config['SECRET_KEY'] = 'yandexlyceum_secret_key'


@app.route('/login', methods=['POST', 'GET'])
def login():
        if request.method == 'GET':
            return render_template('login.html', title='Please fill in this form to sign in an account:')
        elif request.method == 'POST':
            um = UsersModel(db.get_connection())
            um.init_table()
            print('um created in login')
            print(um.get_all())
            if um.exists(request.form['email'], request.form['pswd']):
                username = um.get_username(request.form['email'])
                session['username'] = username
                print('got here')
                return redirect('/main')
            else:
                return render_template('login.html', title='Wrong email or password')



@app.route('/sign_up', methods=['POST', 'GET'])
def sign_up():
    if request.method == 'GET':
        return render_template('sign_up.html', title='Please fill in this form to create an account:')
    elif request.method == 'POST':
        um = UsersModel(db.get_connection())
        um.init_table()
        print(um.get_all())
        print('um created in sign up')
        um.insert(request.form['email'], request.form['uname'], request.form['pswd'])
        session['username'] = request.form['uname']
        print('if statement')
        return redirect('/main')

            # return render_template('sign_up', title='Specified account already exists. Log in with it or create new one')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/account')
def account():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'GET':
        return render_template('account.html', username=session['username'])


@app.route('/about')
def about():
    if request.method == 'GET':
        return render_template('about.html')


@app.route('/delete_news/<int:news_id>', methods=['GET'])
def delete_news(news_id):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.delete(news_id)
    return redirect("/index")


@app.route('/main', methods=['POST', 'GET'])
def main():
    # if 'username' not in session:
    #     return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.init_table()
    # nm.delete_all()
    if request.method == "POST":
        content = request.form["comment"]
        # content = request.files["uploadingfiles"]

        print(session['username'])
        nm.insert(str(time.asctime(time.localtime(time.time()))), content, session['username'])  # CHANGE CHANGE to user id

        return redirect("/main")
    else:
        return render_template('home.html', title='Добавление новости', username=session['username'], news=nm.get_all())


@app.route('/user/<nickname>', methods=['GET'])
def show_users_news(nickname):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.init_table()
    if request.method == "GET":
        return render_template('home.html', title=('All news of' + nickname),
                               username=session['username'], news=nm.get_all(nickname))


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')