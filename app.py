from flask import Flask, render_template, request, redirect, url_for, flash
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo, ValidationError
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os
from wtforms.widgets import TextArea
#from . import create_user_db

app = Flask(__name__)

#Add Database
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get("MYSQL_DB_URI")

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
        return '<User %r>' % self.username

class Bash(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    bash_title = db.Column(db.String(100), nullable=False)
    bash_descr = db.Column(db.String(1000), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    #Create String
    def __repr__(self):
        return '<User %r>' % self.username

#Secret
app.config['SECRET_KEY'] = os.environ.get("SECRET_KEY")

# Create a Form Class
class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    submit = SubmitField("Login")

class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    email = StringField("Email", validators=[DataRequired(), Length(min=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField(
    label=('Confirm Password'),
    validators=[DataRequired(message='*Required'),
    EqualTo('password', message='Both password fields must be equal!')])
    create_account = SubmitField("Create Account")

class CreateBashForm(FlaskForm):
    bash_title = StringField("Title", validators=[DataRequired(), Length(min=3)])
    bash_descr = TextAreaField("Bash", validators=[DataRequired(), Length(min=4)], widget=TextArea())
    create_bash = SubmitField("Create Bash")

class UpdateBashForm(FlaskForm):
    bash_title = StringField("Title", validators=[DataRequired(), Length(min=3)])
    bash_descr = StringField("Bash", validators=[DataRequired(), Length(min=4)])
    update_bash = SubmitField("Update Bash")

class UpdateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired(), Length(min=3)])
    email = StringField("Email", validators=[DataRequired(), Length(min=8)])
    password = PasswordField("Password", validators=[DataRequired(), Length(min=4)])
    confirm_password = PasswordField(
    label=('Confirm Password'),
    validators=[DataRequired(message='*Required'),
    EqualTo('password', message='Both password fields must be equal!')])
    update_account = SubmitField("Update Account")

@app.route('/', methods = ['GET'])
def index():
    return render_template('index.html')

# localhost/john
#route for Profile
@app.route('/<username>',  methods =['GET', 'POST'])
def user(username):

    #TO DO
    # SELECT * users where id
    return render_template('user.html', username=username)

@app.route('/bash/all',  methods = ['GET', 'POST'])
def bash():
    # bash_id = 1
    # bash_decr = 'This is my first bash'
    # bash_title = "Nothing but a Title"
    bashes = Bash.query.order_by(Bash.created_at)

    return render_template('bash.html', bashes=bashes)

@app.route('/bash/create',  methods = ['GET', 'POST'])
def create_bash():
    form = CreateBashForm()
    # bash_id = 1
    bash_decr = None
    bash_title = None
    bashes = Bash.query.order_by(Bash.created_at)

    if request.method ==  'POST':
        if form.validate_on_submit():
            bash = Bash(bash_title=form.bash_title.data, bash_descr=form.bash_descr.data)
            db.session.add(bash)
            db.session.commit()
            bash_title = form.bash_title.data
            bash_descr = form.bash_descr.data
            bashes = Bash.query.order_by(Bash.created_at)
            flash("Bash created successfully")
            return redirect(url_for('bash', bashes=bashes))
        else:
            flash(form.errors.items())
            return render_template('create-bash.html',form=form)
    elif request.method == 'GET':
        bash_title = form.bash_title.data
        bash_descr = form.bash_descr.data
        bashes = Bash.query.order_by(Bash.created_at)

        return render_template('create-bash.html', form=form, create=True, bashes=bashes)
    else:
        return "Something went wrong"


@app.route('/user/<int:id>/update/', methods = ['PUT', 'GET', 'POST'])
def update_user(id):
    form = UpdateUserForm()
    username_to_update = Users.query.get_or_404(id)
    password_to_update = Users.query.get_or_404(id)
    email_to_update = Users.query.get_or_404(id)
    if not id:
        return "No ID was given"
    if request.method == 'POST':
        username_to_update.username = request.form['username']
        password_to_update.username = request.form['password']
        email_to_update.username = request.form['email']
        try:
            db.session.commit()
            flash(f"User {id} updated successfully")
            return render_template('update-user.html', form=form, username_to_update=username_to_update, email_to_update=email_to_update, password_to_update=password_to_update)
        except:
            flash(f"Error! Looks there was an error.. try again!")
            return render_template('update-user.html', form=form, username_to_update=username_to_update, email_to_update=email_to_update, password_to_update=password_to_update)
    else:
        return render_template('update-user.html', form=form, username_to_update=username_to_update, email_to_update=email_to_update, password_to_update=password_to_update)

@app.route('/bash/<int:id>/update',  methods = ['GET', 'POST'])
def update_bash(id):
    form = UpdateBashForm()
    bash_to_update = Users.query.get_or_404(id)
    if not id:
        return "No ID was given"
    if request.method == 'POST':
        bash_to_update.bash_title = request.form['bash_title']
        bash_to_update.bash_descr = request.form['bash_descr']
        try:
            db.session.commit()
            flash(f"Bash {id} updated successfully")
            return render_template('update-bash.html', form=form, bash_to_update=bash_to_update)
        except:
            flash(f"Error! Looks there was an error.. try again!")
            return render_template('update-bash.html', form=form, bash_to_update=bash_to_update)
    else:
        return render_template('update-bash.html', form=form, bash_to_update=bash_to_update)
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
                user = Users(username=form.username.data, password=form.password.data,
                    email=form.email.data)
                db.session.add(user)
                db.session.commit()
            username = form.username.data
            email = form.email.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            our_users = Users.query.order_by(Users.created_at)
            flash("User added successfully")
            return redirect(url_for('user', username=username, password=password, confirm_password=confirm_password,email=email))
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

