from flask import Flask, render_template , request , redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///todo.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Todo(db.Model): #M should be capital in model
    sno = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(300), nullable=False)
    desc = db.Column(db.String(300), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"{self.sno} - {self.title}"

@app.route("/" , methods=['GET' , 'POST'])   #taking entries from the form into the database
def home():
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo(title=title , desc = desc)
        db.session.add(todo)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html' , alltodo=alltodo)   #returning the databse to the index.html to print in table

@app.route("/show")
def products():
    alltodo = Todo.query.all()
    print(alltodo)
    return "You can select the following products!"

@app.route("/update/<int:sno>", methods=['GET' , 'POST'])
def update(sno):
    if request.method == 'POST':
        title = request.form['title']
        desc = request.form['desc']
        todo = Todo.query.filter_by(sno = sno).first()
        todo.title = title
        todo.desc = desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo = Todo.query.filter_by(sno = sno).first()
    return render_template('update.html' , todo=todo)

@app.route("/delete/<int:sno>")
def delete(sno):
    todo = Todo.query.filter_by(sno = sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

if __name__ == "__main__":
    app.run(debug=True, port=8000)
