# from flask_wtf import FlaskForm
# from wtforms import StringField, PasswordField, BooleanField, SubmitField, TextAreaField
# from wtforms.validators import DataRequired
from flask import Flask, render_template, redirect, request, session
import time
# import requests
from news_model import NewsModel
from db import DB
from users_model import UsersModel

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
            print(um.get_all())
            if um.exists(request.form['email'], request.form['pswd']):
                username = um.get_username(request.form['email'])
                session['username'] = username
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
        um.insert(request.form['email'], request.form['uname'], request.form['pswd'])
        session['username'] = request.form['uname']
        print(um.get_all())
        return redirect('/main')

        # return render_template('sign_up', title='Specified account already exists. Log in with it or create new one')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


@app.route('/my_page')
def my_page():
    if 'username' not in session:
        return redirect('/login')
    if request.method == 'GET':
        nm = NewsModel(db.get_connection())
        nm.init_table()
        um = UsersModel(db.get_connection())
        um.init_table()
        em = um.get_email(session['username'])
        uname = session['username']
        return render_template('account.html', username=uname, news=nm.get_all(uname),
                               email=em)


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
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.init_table()
    # nm.delete_all()
    if request.method == "POST":
        content = request.form["comment"]
        # content = request.files["uploadingfiles"]

        print(session['username'])
        nm.insert(str(time.asctime(time.localtime(time.time()))), content, session['username'])

        return redirect("/main")
    else:
        return render_template('home.html', title='Добавление новости', username=session['username'], news=nm.get_all())


@app.route('/user/<uname>', methods=['GET'])
def show_user(uname):
    if 'username' not in session:
        return redirect('/login')
    nm = NewsModel(db.get_connection())
    nm.init_table()
    um = UsersModel(db.get_connection())
    um.init_table()
    em = um.get_email(session['username'])
    if request.method == "GET":
        return render_template('account.html', username=uname, news=nm.get_all(uname), email=em)


if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
