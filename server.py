from flask import Flask, render_template, redirect, request, url_for, session
import sqlite3
from markupsafe import escape
import uuid

app = Flask(__name__)

app.secret_key = b'Z\xb3Q\x93\xfd\xf1\xfe\x1c\x8c\xc2\x1c\x8eDlZ+'

@app.route('/login')
def login():
    if 'username' in session:
        return redirect(url_for('index'))
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
        if ans[0][0] == password:
            crsr.execute("SELECT full_name FROM cred WHERE username == '{}'".format(name))
            ans1 = crsr.fetchall()
            conn.close()
            session['username'] = ans1[0][0]
            session['email'] = name
            return redirect(url_for('index'))
        else:
            return redirect(url_for('login'))
    else:
        return "BAD REQUEST"

@app.route('/sign_Up', methods=['GET', 'POST'])
def sign_Up():
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('sign_up.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    if request.method == 'POST':
        full_name = request.form['u_full_name']
        email = request.form['uemail']
        upass = request.form['upass']
        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("INSERT INTO cred (username, password, full_name) VALUES ('{}', '{}', '{}')".format(email, upass, full_name))
        conn.commit()
        conn.close()
        return redirect(url_for('login'))
    else:
        return "BAD REQUEST"

@app.route('/checkEmail', methods=['POST'])
def checkEmail():
    if request.method == 'POST':
        email = request.args.get('email')
        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("SELECT username FROM cred WHERE username=='{}'".format(email))
        ans = crsr.fetchall()
        conn.close()
        if (len(ans) == 0):
            return "False"
        else:
            return "True"

@app.route('/')
def index():
    if 'username' in session:
        return render_template('index.html', full_name=escape(session['username']))
    else:
        return redirect(url_for('login'))

@app.route('/new_project')
def new_project():
    if 'username' in session:
        return render_template('new_project.html', full_name=escape(session['username']))

@app.route('/create_project', methods=['POST'])
def create_project():
    if request.method == 'POST':
        project_id = uuid.uuid4()
        project_owner = escape(session['email'])
        project_name = request.form['projectName']
        project_des =  request.form['projectdes']
        project_dead = request.form['projectdead']
        project_team = request.form['projectteam']

        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("INSERT INTO project(ProjectID, Name, Description, Deadline, owner, team_member) VALUES ('{}', '{}', '{}', '{}', '{}', '{}')".format(project_id, project_name, project_des, project_dead, project_owner, project_team))
        conn.commit()
        conn.close()
        return redirect(url_for('index'))
    else:
        return "Bad Request"

@app.route('/project_dash', methods=['POST'])
def project_dash():
    if ((request.method == 'POST') and ('username' in session)):
        return render_template('project_dashboard.html')

@app.route('/logout')
def logout():
    session.pop('username',None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()

