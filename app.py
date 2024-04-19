
import random

from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import FileField, PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo,Email,DataRequired
from flask_sqlalchemy import SQLAlchemy 
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash


app = Flask(__name__)
app.secret_key = 'your_secret_key'





app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///users.db'
app.config['SECRET_KEY'] = "my super secret key  no one is supposed to know"

# Initialize The Database
db = SQLAlchemy(app)
app.app_context().push() 
# στο shell python from app import app    from app import db    db.create_all

#---------------------------------------------------------------
# Create Model
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200), nullable=False)
    score = db.Column (db.Integer, nullable=False)

	
class KeyboardForm(FlaskForm):
    letter = StringField("letter")



class UserForm(FlaskForm):
    email= StringField("Email", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    phone = StringField("Phone")
    pw = PasswordField("Password",validators=[DataRequired()])
    
    #pw2 = PasswordField("Password",validators=[DataRequired() , EqualTo('pw') ])
    submit = SubmitField("Submit")





class Question(db.Model):
    id = db.Column(db.Integer, primary_key=True) 
    question_text = db.Column(db.String(255), unique=True, nullable=False)
    option_A = db.Column(db.String(100), nullable=False)
    option_B = db.Column(db.String(100), nullable=False)
    option_C = db.Column(db.String(100), nullable=False)
    option_D = db.Column(db.String(100), nullable=False)
    correct_answer = db.Column(db.String(1), nullable=False)


  
#---------------------------------------------------------------
letters = [
    'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P',
    'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L',
    'Z', 'X', 'C', 'V', 'B', 'N', 'M'
]
str = 'QWER'
playing = ['_ ' * len(str)]
wrongs = 5
@app.route('/', methods=['GET','POST'])
def play():
        global wrongs
        if request.method == 'POST': 
            form = KeyboardForm() 
            print (form.data)
            print (form.letter.data)
              
            position = str.find(form.letter.data)
            if position == -1:     
                flash ("wrong")
                wrongs -= 1
            else : 
                playing[position]= form.letter.data
            
            
        return render_template('index.html' , form = form, str=None, x = letters, playing=playing)
            

@app.errorhandler(404)
def page_not_found(e):    
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)
def page_not_found(e):    
    return render_template('500.html'), 404





if __name__ == '__main__':
    app.run(debug=True)
    