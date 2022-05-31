from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'

#initialize Database
db = SQLAlchemy(app)

#CREATE MODEL
class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Create String
    def __repr__(self):
        return '<Name %r>' % self.name 

#Secret
app.config['SECRET_KEY'] = "lkjhgfdsa!3"

# Create a Form Class
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Submit")

class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    email = StringField("Email", validators=[DataRequired(), Length(min=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField(
    label=('Confirm Password'), 
    validators=[DataRequired(message='*Required'),
    EqualTo('password', message='Both password fields must be equal!')])
    create_account = SubmitField("Create Account")

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

# localhost:5000/user/john
@app.route('/user/<username>',  methods =['GET', 'POST'])
def user(username):
    
    #TO DO 
    # SELECT * users where id 
    return render_template('user.html', username=username)

@app.route('/bash/<id>',  methods = ['GET', 'POST'])
def bash(id):
    bash = 'This is my first bash'
    bash_title = "Nothing but a Title"
    username = "Daddy Yankee"
    return render_template('bash.html', bash_id=id, bash=bash, bash_title=bash_title, username=username)

# invalid URL
@app.errorhandler(404)
def page_not_found(e):
	return render_template("404.html"), 404

#Internal Server Error
@app.errorhandler(404)
def page_not_found(e):
	return render_template("500.html"), 500

@app.route('/login', methods = ['GET', 'POST'])
def login():
    username = None
    password = None

    form = LoginForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            return redirect(url_for('user', username=username, password=password))
        else:
            return render_template('login.html', form=form)
    elif request.method == 'GET':
        username = form.username.data
        password = form.password.data

        return render_template('login.html', username=username, form=form, password=password)  
    else: 
        return flash("Something went wrong!")

@app.route('/user/create', methods = ['GET', 'POST'])
def create_user():
    username = None
    password = None
    email = None
    create = True
    form = CreateUserForm()

    if request.method ==  'POST':
        if form.validate_on_submit():
            user = Users.query.filter_by(username=form.username.data).first()
            if user is None:
                user =Users(username=form.username.data, password=form.password.data,
                    email=form.email.data)
                db.session.add(user)
                db.session.commit()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            flash("User added successfully")
            return redirect(url_for('user', username=username, password=password, confirm_password=confirm_password,email=email, our_users=our_users))
        else:
            flash(form.errors.items())
            return render_template('create-user.html',form=form)
    elif request.method == 'GET':
        user_name = form.username.data
        password = form.password.data
        our_users = Users.query.order_by(Users.created_at)

        return render_template('create-user.html', form=form, create=True, our_users=our_users)
    else:
        return "Something went wrong"        

def get_db_connection():
    con = ""
    return con

    
