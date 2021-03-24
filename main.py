from flask import Flask,render_template,session,request,redirect,flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="mysql+mysqlconnector://root:@localhost/codingworld"
app.config['SECRET_KEY'] = "saris"
db=SQLAlchemy(app)

class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    description=db.Column(db.String(500),nullable=False)
    date=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)->str:
        return f"{self.sno}-{self.title}"

@app.route('/', methods=['GET','POST'])
def home():
    if(request.method=="POST"):
        title=request.form['title']
        desc=request.form['desc']
        ftodo=Todo(title=title,description=desc)
        db.session.add(ftodo)
        db.session.commit()
    allTodo=Todo.query.all()
    return render_template("index.html", allTodo=allTodo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo=Todo.query.filter_by(sno=sno).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect("/")

@app.route('/update/<int:sno>',methods=['GET','POST'])
def update(sno):
    if(request.method=='POST'):
        title=request.form['title']
        desc=request.form['desc']
        todo=Todo.query.filter_by(sno=sno).first()
        todo.title=title
        todo.description=desc
        db.session.add(todo)
        db.session.commit()
        return redirect("/")
    todo=Todo.query.filter_by(sno=sno).first()
    return render_template("update.html",todo=todo)

@app.route("/about")
def about():
    flash("Currently this page is not working ")
    return render_template("about.html")
app.run(debug=True)