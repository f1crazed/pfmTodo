from flask import Flask, url_for
from flask import render_template
from flask import request, redirect
from wtforms import Form, TextField, DateField, validators
from pymongo import MongoClient
from bson.objectid import ObjectId
from datetime import datetime
import platform
import urllib.parse

app = Flask(__name__)
app.secret_key = 'development key'
pvrsn = platform.python_version()
username = urllib.parse.quote_plus('pfmtodouser')
password = urllib.parse.quote_plus('p4ssw0rd')
mongo_url = 'mongodb://%s:%s@mongodb-service' % (username, password)

class Todo():
    def __init__(self):
        self._id = ObjectId()
        self.task_text = ""
        self.due_date = None
        self.create_date = None
        self.complete_date = None
    def Set(self, obj):
        self._id = obj['_id']
        self.task_text = obj['task_text']
        self.due_date = obj['due_date']
        self.create_date = obj['create_date']
        self.complete_date = obj['complete_date']

class CreateTodoForm(Form):
    task = TextField("Task:", validators=[validators.required()])
    due_date = DateField("Due Date:", validators=[validators.required()])




@app.route("/")
@app.route("/index")
def index():
    client = MongoClient(mongo_url)
    db = client.pfmTodo
    return_todos = db.todos.find({'complete_date' : None })
    todos = []
    if return_todos.count() > 0:
        for obj in return_todos:
            t = Todo()
            t.Set(obj)
            todos.append(t)

    return render_template('index.html', todos=todos, pvrsn=pvrsn)



@app.route("/todoscompleted")
def todoscompleted():
    client = MongoClient(mongo_url)
    db = client.pfmTodo
    return_todos = db.todos.find({'complete_date' :{"$ne":None} })
    todos = []
    if return_todos.count() > 0:
        for obj in return_todos:
            t = Todo()
            t.Set(obj)
            todos.append(t)

    return render_template('completed.html', todos=todos)

@app.route("/create", methods = ['GET', 'POST'])
def createtodo():
    form = CreateTodoForm(request.form)
    if request.method == 'GET':
        title = "Create"
        return render_template('createtodo.html', title=title, form=form)
    if request.method == 'POST':
        if form.validate():
            t = Todo()
            t.task_text = form.task.data
            t.due_date = form.due_date.data.strftime('%m-%d-%Y')
            t.create_date = datetime.now().strftime('%m-%d-%Y')
            client = MongoClient(mongo_url)
            db = client.pfmTodo
            db.todos.insert(t.__dict__)
        return redirect(url_for('index'))


@app.route("/completed/<id>", methods = ['GET'])
def completed(id):
    client = MongoClient(mongo_url)
    db = client.pfmTodo
    returnBSONObject = db.todos.find_one({'_id' : ObjectId(id)})
    todo = Todo()
    todo.Set(returnBSONObject)
    todo.complete_date = datetime.now().strftime('%m-%d-%Y')
    db.todos.update({'_id' : ObjectId(id)}, todo.__dict__)
    return redirect(url_for("index"))

if __name__ == '__main__':
    app.run()
