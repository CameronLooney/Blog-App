# The routes are the different URLs that the application implements.
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

from app import app
from flask import render_template, flash, redirect, url_for
from app.form import LoginForm
from flask_login import current_user, login_user
from app.models import User


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

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if they are logged in stop them from going back to log in page
    # current_user variable comes from Flask-Login and can be used at any time
    # during the handling to obtain the user object that represents the client of the request
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        # filter by will only include matching usernames
        # first will return user or none if the user doesnt exist
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        return redirect(url_for('index'))
    return render_template('login.html', title='Sign In', form=form)

