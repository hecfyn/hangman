
from wtforms.widgets import HTMLString, html_params, Input
from wtforms.widgets import  html_params
from wtforms import HiddenField, widgets
from flask import Flask, render_template, flash, request, redirect, url_for, session
from flask_wtf import FlaskForm
from sqlalchemy import desc
from wtforms import FileField, PasswordField, StringField, SubmitField
from wtforms.validators import EqualTo,Email,DataRequired
from flask_sqlalchemy import SQLAlchemy 


from wtforms import Form, StringField


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


str = 'FALL'
class KeyboardForm(FlaskForm):
    letter = StringField("Letter" )
    hidden_field = HiddenField(default=str)


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
letter_dict = {letter: True for letter in letters}

playing = []
for i in range(len(str)):
    playing.append('_')
wrongs = 5
@app.route('/', methods=['GET','POST'])
def play():
        global wrongs
        global playing

        form = KeyboardForm()
        positions = []

        if request.method == 'POST':
            print (playing)
            
            letter = request.form['button']
            letter_dict[letter] = False  # Mark the letter as guessed
            print(letter)
            # Check if the guessed letter is in the word
            if letter in str:
                for i, char in enumerate(str):
                    if char == letter:
                        playing[i] = char  # Update playing at the correct positions
            elif wrongs != 0 :
                flash("Wrong guess!")
                
                wrongs -= 1  # Decrement the wrongs count
            else : 
                flash('You lost!')

        return render_template('index.html', form=form, x=letter_dict, playing=playing, wrongs=wrongs)
            
        
       


@app.errorhandler(404)
def page_not_found(e):    
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)
def page_not_found(e):    
    return render_template('500.html')





if __name__ == '__main__':
    app.run(debug=True)
    