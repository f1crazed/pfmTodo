from flask import Flask, url_for
from flask import render_template
from flask import request, redirect
from wtforms import Form, TextField, DateField, validators
from pymongo import MongoClient
from datetime import datetime

class Todo():
    def __init__(self):
        self.task_text = ""
        self.due_date = None
        self.create_date = None
        self.complete_date = None

class CreateTodoForm(Form):
    task = TextField("Task: ", validators=[validators.required()])
    due_date = DateField("Due Date:", validators=[validators.required()])

app = Flask(__name__)
app.secret_key = 'development key'


@app.route("/")
@app.route("/index")
def index():
    return render_template('index.html')

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
            client = MongoClient()
            db = client.pfmTodo
            db.todos.insert(t.__dict__)
            print form.task.data
            print form.due_date.data
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run()