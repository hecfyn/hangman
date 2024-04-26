
from wtforms.widgets import HTMLString, html_params, Input
from wtforms.widgets import  html_params
from wtforms import widgets
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


class ButtonWidget(Input):
    input_type = 'button'

    def __call__(self, field, **kwargs):
        """
        This method is the callback function for the ButtonWidget class.
        It generates the HTML markup for a button widget and returns it as a string.

        Parameters:
            field (wtforms.fields.StringField): The StringField instance that this widget is associated with.
            **kwargs: Additional keyword arguments that can be used to customize the button.

        Returns:
            HTMLString: The HTML markup for the button.
        """
        # Retrieve the 'i' value if passed in kwargs
        i = kwargs.pop('i', None)

        # Set default values for kwargs
        kwargs.setdefault('id', field.id)  # Set the id attribute of the button
        kwargs.setdefault('onclick', "disableButton('" + field.id + "')")  # Set the onclick event of the button
        kwargs.setdefault('class', 'form-check-input btn btn-success btn-letter')  # Set the class attribute of the button
        kwargs.setdefault('name', field.name)  # Set the name attribute of the button
        kwargs.setdefault('value', field._value())  # Set the value of the button
        kwargs.setdefault('required', True)  # Set the required attribute of the button

        # Generate the HTML markup for the button and return it
        return HTMLString('<button %s>%s</button>' % (html_params(type=self.input_type, **kwargs), i))


	
class KeyboardForm(FlaskForm):
    letter = StringField("Letter" , widget=ButtonWidget())
    


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
        form = KeyboardForm()
        print (form.letter.data)
        # if request.method == 'POST': 
        #     print (form.data)
        #     position = str.find(form.letter.data)
        #     if position == -1:     
        #         flash ("wrong")
        #         wrongs -= 1
        #     else : 
        #         playing[position]= form.letter.data
            
            
        return render_template('index.html' , form = form, str=None, x = letters, playing=playing)
       


@app.errorhandler(404)
def page_not_found(e):    
    return render_template('404.html'), 404

#internal server error
@app.errorhandler(500)
def page_not_found(e):    
    return render_template('500.html')





if __name__ == '__main__':
    app.run(debug=True)
    