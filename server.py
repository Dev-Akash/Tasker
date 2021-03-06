from flask import Flask, render_template, redirect, request, url_for, session
import sqlite3
from markupsafe import escape
import uuid
import json
import createDatabase as cd

app = Flask(__name__)
cd.createDatabase()
#This key must be changed before deploying it and must be unique
app.secret_key = b'Z\xb3Q\x93\xfd\xf1\xfe\x1c\x8c\xc2\x1c\x8eDlZ+'

'''
Here are all routes listed which can be called.
In all routes some of them are directly accessible 
using GET request while some are internal API require
POST request.
'''
@app.route('/login')
def login():
    '''
    Lauched by '/login' route request and renders
    Login page to the user if not logged in else
    render the index page where all project of user
     are listed.
    '''
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('login_page.html')

@app.route('/checkUser', methods=['POST'])
def checkUser():
    '''
    CheckUser method gets activate on call of 
    '/checkUser' route which is called while logging in.
    This method checks whether a user is valid or not and
    redirect it to the index page if valid else redirect
    again to the login page
    '''
    if request.method == 'POST':
        name = request.form['uname']
        password = request.form['upass']

        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("SELECT password FROM cred WHERE username == '{}'".format(name))
        ans = crsr.fetchall()
        if not (len(ans) == 0):
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
    '''
    Sign Up function gets activated on '/sign_up request
    and renders the sign_up html page to sign_up the user
    if the user not already signed in.
    '''
    if 'username' in session:
        return redirect(url_for('index'))
    return render_template('sign_up.html')

@app.route('/add_user', methods=['POST'])
def add_user():
    '''
    The add_user function gets triggered when a new
    user signs up. This function save all the details
    provided by the user to the database.
    '''
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
    '''
    This function get triggers when the user attempt
    to sign up. This function is used check that the 
    email used at the sign up is present in the database
    or not. If yes the send True else Fasle which will
    render the red border around email input by javascript
    accordingly.
    '''
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
    '''
    This is the main route which will be triggered
    when a user comes to the website. This page will
    render the Login page if user is not logged in else
    will render the index page.
    '''
    if 'username' in session:
        return render_template('index.html', full_name=escape(session['username']))
    else:
        return redirect(url_for('login'))

@app.route('/new_project')
def new_project():
    '''
    This function gets triggered when user request for 
    new project and this will render the html for filling
    the details of the project.
    '''
    if 'username' in session:
        return render_template('new_project.html', full_name=escape(session['username']))

@app.route('/create_project', methods=['POST'])
def create_project():
    '''
    This function gets triggered when user submit the 
    request for the creation of new project. This function
    add all the information of the poject in the database
    table for projects and then render the index page.
    '''
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

@app.route('/fetchProjects', methods=['POST'])
def fetchProjects():
    '''
    This function will be triggered by XMLHttpRequest
    asking for the projects associated with user 
    account. This function will return a JSON string
    for owned projects as well as other projects.
    '''
    if request.method == 'POST':
        email = session['email']
        #Creating JSON Data format
        root = '{ "owned" : [], "associated":[]}'
        root_json = json.loads(root)
        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("SELECT * FROM project WHERE owner == '{}'".format(email))
        ans = crsr.fetchall()
        
        #Adding JSON data for owned projects
        temp = root_json['owned']
        for i in ans:
            project_id = i[0]
            project_name = i[1]
            project_des = i[2]
            project_dead = i[3]
            project_owner = i[4]
            project_team = i[5]

            data = {"project_id": project_id,
            "project_name":project_name,
            "project_des":project_des,
            "project_dead":project_dead,
            "project_owner":project_owner,
            "project_team":project_team}

            temp.append(data)
        root = json.dumps(root_json)

        #Adding JSON data for Associated projects
        root_json = json.loads(root)
        crsr.execute("SELECT * FROM project WHERE team_member LIKE '%{}%'".format(email))
        ans = crsr.fetchall()
        conn.close()
        temp = root_json['associated']
        for i in ans:
            project_id = i[0]
            project_name = i[1]
            project_des = i[2]
            project_dead = i[3]
            project_owner = i[4]
            project_team = i[5]
            
            data = {"project_id": project_id,
            "project_name":project_name,
            "project_des":project_des,
            "project_dead":project_dead,
            "project_owner":project_owner,
            "project_team":project_team}

            temp.append(data)
        root = json.dumps(root_json)
        return root

@app.route('/project_dash', methods=['GET','POST'])
def project_dash():
    '''
    This would be the page for rendering all the information
    of the project selected and also helps to added data using
    the XMLHttpRequest in javascript.
    '''
    if ('username' in session):
        id = request.args.get('id')
        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("SELECT owner, team_member FROM project WHERE ProjectID =='{}'".format(id))
        ans = crsr.fetchall()
        allow = False
        for i in ans:
            if i[0] == str(escape(session['email'])):
                allow = True
            elif str(escape(session['email'])) in i[1]:
                allow = True
        if allow:
            return render_template('project_dashboard.html', full_name=escape(session['username']), id=id)
        else:
            return "BAD REQUEST"
    else:
        return "BAD REQUEST"

@app.route('/submitTask', methods=["POST"])
def submitTask():
    '''
    This function will take the value of the task 
    using AJAX call and submit it into the database
    '''
    if ('username' in session) and (request.method=="POST") :
        name = request.args.get("name")
        desc = request.args.get("desc")
        assig = request.args.get("assig")
        dead = request.args.get("dead")
        project_id = request.args.get("project_id")

        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("INSERT INTO Task VALUES ('{}', '{}', '{}', '{}', '{}')".format(project_id,name,desc,assig,dead))
        conn.commit()
        conn.close()
        return "ok"
    else:
        return "not ok"

@app.route("/submitStage", methods=["POST"])
def submitStage():
    '''
    This function will take the value of the stage form 
    using AJAX call and submit it into the database
    '''
    if ('username' in session) and (request.method=="POST") :
        name = request.args.get("name")
        desc = request.args.get("desc")
        tasks = request.args.get("tasks")
        rewards = request.args.get("rewards")
        project_id = request.args.get("project_id")

        print(name, desc, tasks, rewards, project_id)
        conn = sqlite3.connect('Tasker.db')
        crsr = conn.cursor()
        crsr.execute("INSERT INTO Stage VALUES ('{}', '{}', '{}', '{}', '{}')".format(project_id,name,desc,tasks,rewards))
        conn.commit()
        conn.close()

        return "ok"
    else:
        return "not ok"

@app.route('/logout')
def logout():
    '''
    This function gets triggered when the user hits
    the logout button or request for '/logout'. 
    This function remove all the stored session
    '''
    session.pop('username', None)
    session.pop('email', None)
    return redirect(url_for('index'))

if __name__ == "__main__":
    app.run()

