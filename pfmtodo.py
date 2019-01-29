from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

@app.route("/create", methods = ['GET', 'POST'])
def createtodo():
    if request.method == 'GET':
        title = "Create"
    if request.method == 'POST':
        ""
    return render_template('createtodo.html', title=title)

if __name__ == '__main__':
    app.run()