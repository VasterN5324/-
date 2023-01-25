from flask import Flask, flash, render_template, url_for, request, redirect, session, logging
from forms import LoginForm
from forms import RegistrationForm
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from werkzeug.security import check_password_hash, generate_password_hash






app = Flask(__name__)

app.config['SECRET_KEY'] = 'hardsecretkey'

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///notes_db.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)





class User(db.Model):   
    id = db.Column(db.Integer, primary_key = True) 
    username = db.Column(db.String(80))
    email = db.Column(db.String(120))
    password = db.Column(db.String(80))

    def __init__(self, username, password):
        self.username = username
        self.password = password

class Notes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = False)
    text = db.Column(db.Text, nullable = False)
    date = db.Column(db.DateTime, default = datetime.utcnow)


   
    


with app.app_context():
    db.create_all()

@app.route('/')
def index():
    return render_template("index.html")    


@app.route('/login' , methods = ['GET', 'POST'])
def Login():
    form = LoginForm()
 
    if form.validate_on_submit():
        if request.form['username'] != '111' or request.form['password'] != '111':
            flash("Invalid Credentials, Please Try Again")
 
 
        else:
            return redirect(url_for('index'))
 
 
 
    return render_template('login.html', form = form)    


@app.route('/register' , methods = ['GET', 'POST'])
def register():
    form = RegistrationForm()
 
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method = 'sha256')
        username = form.username.data
        password = hashed_password
 
 
        new_register =User(username=username, password=password)
 
        db.session.add(new_register)
 
        db.session.commit()
 
        flash("Registration was successfull, please login")
 
        return redirect(url_for('Login'))
 
 
    return render_template('register.html', form=form)    



@app.route('/notes')
def note():
   notes = Notes.query.order_by(Notes.date.desc()).all()
   return render_template("notes.html", notes=notes)



@app.route('/notes/<int:id>')
def note_extend(id):
   note = Notes.query.get(id)
   return render_template("note_extend.html", notes=note)


@app.route('/notes/<int:id>/delete')
def note_delete(id):
   note = Notes.query.get_or_404(id)
   try:

    db.session.delete(note)
    db.session.commit()
    return redirect('/notes')
   except:
    return "При удалении заметки произошла ошибка"

   return render_template("note_extend.html", notes=note)   



@app.route('/notes/<int:id>/edit', methods = ['POST', 'GET'])
def note_edit(id):
    note = Notes.query.get(id)  
    if request.method == "POST":
        note.title = request.form['title']
        note.text = request.form['text']
        
        
        
        try:
           db.session.commit()
           return redirect('/notes')
        except:
           return "При редктировании заметки произошла ошибка"    
    else: 
        return render_template("note_edit.html", notes=note)

      


@app.route('/new-note', methods = ['POST', 'GET'])
def new_note():
    if request.method == "POST":
        title = request.form['title']
        text = request.form['text']
        
        note = Notes(title = title, text = text )
        
        
        try:
           db.session.add(note)
           db.session.commit()
           return redirect('/notes')
        except:
           return "При добавлении заметки произошла ошибка"    
    else:     
        return render_template("new_note.html")





@app.route('/user/notes/<int:id>')
def user(id):
    return "Note #" + str(id)    

if __name__ == "__main__":
    app.run(debug = True)    