from flask import Flask, render_template

app = Flask(__name__)

@app.route('/', methods = ['GET', 'POST'])
def index():
    return render_template('index.html')

# localhost:5000/user/john
@app.route('/user/<username>',  methods = ['GET', 'POST'])
def user(username):
    return render_template('user.html',  username=username)

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


    
