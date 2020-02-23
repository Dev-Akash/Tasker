from flask import Flask, render_template, redirect

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/new_project')
def new_project():
    return render_template('new_project.html')

if __name__ == "__main__":
    app.run()

