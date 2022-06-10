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

    posts = [{
                 'author': {'username'  : 'Cameron'},
                 'body': 'I just a baby'},
             {
                 'author': {'username': 'Megan'},
                 'body': 'Im panicking, im gonna lose me job'}

             ]
    # there are a couple of placeholders for the dynamic content, enclosed in {{ ... }} sections.
    # These placeholders represent the parts of the page that are variable and will only be known at runtime.
    return render_template('index.html', posts = posts)

# new view for login page
from flask import request
from werkzeug.urls import url_parse

@app.route('/login', methods=['GET', 'POST'])
def login():
    # if the user is authenticated then redirect to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    # if the user isnt logged in show them the login form
    form = LoginForm()
    if form.validate_on_submit():
        # if they submit details check if they are correct
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('Invalid username or password')
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html', title='Sign In', form=form)


from flask_login import logout_user
# uses built in logout function ,redirect the user to home page
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

from app import db
from app.form import RegisterForm
# ...
@app.route('/register', methods=['GET', 'POST'])
def register():
    # if user is logged in already send to home page
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegisterForm()
    if form.validate_on_submit():
        # impute details
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        # add user to db
        db.session.add(user)
        db.session.commit()
        flash('Welcome to the Blog {}'.format(form.username.data))
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)