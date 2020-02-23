from flask import Flask, render_template, redirect, request, url_for
import sqlite3

app = Flask(__name__)

@app.route('/')
def login():
    return render_template('login_page.html')

@app.route('/checkUser', methods=['POST'])
def checkUser():
    if request.method == 'POST':
        name = request.form['uname']
        password = request.form['upass']

        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("SELECT password FROM cred WHERE username == '{}'".format(name))
        ans = crsr.fetchall()
        conn.close()
        if ans[0][0] == password:
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))

@app.route('/sign_Up', methods=['GET', 'POST'])
def sign_Up():
    return render_template('sign_up.html')

@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/new_project')
def new_project():
    return render_template('new_project.html')

@app.route('/create_project', methods=['POST'])
def create_project():
    if request.method == 'POST':
        return redirect(url_for('index'))
    else:
        return "Bad Request"

if __name__ == "__main__":
    app.run()

