from flask import Flask, request, render_template, redirect


app = Flask(__name__)


@app.route('/login', methods=['POST', 'GET'])
def login():
        if request.method == 'GET':
            return render_template('index.html')
        elif request.method == 'POST':
            print(request.form['email'])
            print(request.form['password'])
            return redirect('/main')


@app.route('/main', methods=['POST', 'GET'])
def main():
    if request.method == 'GET':
        return render_template('home.html')



if __name__ == '__main__':
    app.run(port=8080, host='127.0.0.1')
