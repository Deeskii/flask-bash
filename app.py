from flask import Flask, render_template, request, redirect, url_for
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = "lkjhgfdsa!3"

# Create a Form Class
class CreateUserForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = StringField("Password", validators=[DataRequired()])
    submit = SubmitField("Submit")


@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

# localhost:5000/user/john
@app.route('/user/<username>',  methods =['GET'])
def user(username):
    #TO DO 
    # SELECT * users where id 
    dee = "whatever hoe"
    return render_template('user.html', username=username, dee=dee)

@app.route('/bash/<id>',  methods = ['GET', 'POST'])
def bash(id):
    bash = 'This is my first bash'
    bash_title = "You ain't shit"
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

    form = CreateUserForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        form.username = ''

    return render_template('login.html', username=username, form=form, password=password)

@app.route('/user/create', methods = ['GET', 'POST'])
def create_user():
    username = None
    password = None
    form = CreateUserForm()

    if request.method ==  'POST':
        username = form.username.data
        password = form.password.data
        form.username = ''
        return redirect(url_for('user', username=username))
    elif request.method == 'GET':
        user_name = form.username.data
        password = form.password.data
            
        return render_template('create-user.html', form=form)
    else:
        return "Something went wrong"        



    
