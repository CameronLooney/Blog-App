# The routes are the different URLs that the application implements.
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

from app import app
from flask import render_template
from app.form import LoginForm


# @app.route decorator creates an association between the URL given as an argument and the function.
# when a web browser requests either of these two URLs,
# Flask is going to invoke this function and pass the return value of it back to the browser as a response
@app.route("/")
@app.route('/index')
def index():
    user = {'username': 'Cameron'}

    posts = [{
                 'author': {'username'  : 'Cameron'},
                 'body': 'I just a baby'},
             {
                 'author': {'username': 'Megan'},
                 'body': 'Im panicking, im gonna lose me job'}

             ]
    # there are a couple of placeholders for the dynamic content, enclosed in {{ ... }} sections.
    # These placeholders represent the parts of the page that are variable and will only be known at runtime.
    return render_template('index.html', user = user, posts = posts)

# new view for login page
@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html', title='Sign In', form=form)

