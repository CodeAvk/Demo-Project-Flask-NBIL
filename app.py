from flask import Flask,render_template,request,redirect,url_for
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.utils import secure_filename
import os


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']="sqlite:///users.db"
# app.config['SQLALCHEMY_TRACK_MODIFICATIONs']=False
db = SQLAlchemy(app)


class Todo(db.Model):
    sno=db.Column(db.Integer,primary_key=True)
    title=db.Column(db.String(200),nullable=False)
    desc=db.Column(db.String(500),nullable=False)
    date_created=db.Column(db.DateTime,default=datetime.utcnow)
    image = db.Column(db.String(200))

    def __repr__(self)-> str:
        return f"{self.sno} - {self.title}"

@app.route('/',methods=['GET','POST'])
def hello_world():
    if request.method=='POST':
        # print(request.form['image'])
        title=request.form['title']
        desc=request.form['desc']
        # Get the uploaded image file
        image = request.files.get('image')

        # Save the file and get the file path
        if image and image.filename != '':
            filename = secure_filename(image.filename)
            image.save(os.path.join('static/uploads', filename))
            image_path = f"uploads/{filename}"  # Relative path to the saved image
        else:
            image_path = None
    
       
         # Create and add the Todo to the database
        todo = Todo(title=f"{title}", desc=f"{desc}", image=image_path)
        db.session.add(todo)
        db.session.commit()
        # Redirect to a GET route to prevent form resubmission on page refresh
        return redirect(url_for('display_todos'))
    
    allTodo=Todo.query.all()
    # print(allTodo)

    return render_template("index.html", allTodo=allTodo)

@app.route('/display')
def display_todos():
    allTodo = Todo.query.all()
    return render_template("index.html", allTodo=allTodo)


@app.route('/show')
def products():
    allTodo=Todo.query.all()
    print(allTodo)
    return f'Here is all to do section --- \n{allTodo}'

@app.route('/update/<int:sno>', methods=['GET', 'POST'])
def update(sno):
    todo = Todo.query.get_or_404(sno)
    if request.method == 'POST':
        todo.title = request.form['title']
        todo.desc = request.form['desc']
        db.session.commit()
        return redirect('/')
    return render_template('update.html', todo=todo)

@app.route('/delete/<int:sno>')
def delete(sno):
    todo_to_delete = Todo.query.get_or_404(sno)
    db.session.delete(todo_to_delete)
    db.session.commit()
    return redirect('/')

if __name__ == "__main__":
    with app.app_context():
        db.create_all()
    app.run(debug=True) # debug =True means what wver the error came it will show in Browser
