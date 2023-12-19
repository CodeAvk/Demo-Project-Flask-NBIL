from flask import Flask,render_template
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///users.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONs']=False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"

@app.route('/')
def hello_world():
    todo=Todo(title="First todo",desc="Start Learning Go")
    db.session.add(todo)
    db.session.commit()
    allTodo=Todo.query.all()
    print(allTodo)

    return render_template("index.html")

@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return f'Here is all to do section --- \n{allTodo}'

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) # debug =True means what wver the error came it will show in Browserp
