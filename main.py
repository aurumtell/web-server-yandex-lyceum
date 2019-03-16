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
            return render_template('login.html')
        elif request.method == 'POST':
            print(request.form['email'])
            print(request.form['password'])
            session['username'] = request.form['email']
            return redirect('/main')


@app.route('/logout')
def logout():
    session.pop('username', 0)
    return redirect('/login')


class AddNewsForm(FlaskForm):
    title = StringField('Заголовок новости', validators=[DataRequired()])
    content = TextAreaField('Текст новости', validators=[DataRequired()])
    submit = SubmitField('Добавить')


@app.route('/account')
def account():
    if request.method == 'GET':
        return render_template('account.html')


@app.route('/about')
def about():
    if request.method == 'GET':
        return render_template('about.html')



# @app.route('/add_news', methods=['GET', 'POST'])
# def add_news():
#     if 'username' not in session:
#         return redirect('/login')
#     # form = AddNewsForm()
#

#     if request.method == "POST":
#         title = request.form["comment"]
#         content = request.form["uploading_files"]
#         print("got here")
#         nm = NewsModel(db.get_connection())
#
#         nm.insert(title, content, session['username'])  # CHANGE CHANGE to user id
#         return redirect("/index")
#     else:
#         return render_template('add_news.html', title='Добавление новости', username=session['username'])


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
        nm.insert(str(time.asctime(time.localtime(time.time()))), content, session['username'])  # CHANGE CHANGE to user id

        print(nm.get_all())

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