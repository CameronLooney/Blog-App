# The routes are the different URLs that the application implements.
# View functions are mapped to one or more route URLs so that Flask knows what logic to execute when a client requests a given URL.

from app import app
from flask import render_template, flash, redirect, url_for
from app.form import LoginForm
from flask_login import current_user,login_user, logout_user,login_required
from app.models import User, Post


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


# dynamic route -> takes the username of user and returns their page or error (as anything can be entered here)
@app.route('/user/<username>')
# as this is the users private page they must log in to enter

@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.posts.order_by(Post.timestamp.desc()).paginate(
        page, app.config['POSTS_PER_PAGE'], False)
    next_url = url_for('user', username=user.username, page=posts.next_num) \
        if posts.has_next else None
    prev_url = url_for('user', username=user.username, page=posts.prev_num) \
        if posts.has_prev else None
    form = EmptyForm()
    return render_template('user.html', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url, form=form)

from datetime import datetime
# before_request decorator will execute this block before any view function is run
@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()


from app.form import EditProfile
@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfile(current_user.username)
    if form.validate_on_submit():
        # if form is true we assign the new data to user object
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        # commit changes to our db
        db.session.commit()
        flash('Your Profile has been updated')
        return redirect(url_for('edit_profile'))
    # when form is requested for first time (GET method) populate fields with current data
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html', title='Edit Profile',
                           form=form)


from app.form import EmptyForm
@app.route('/follow/<username>', methods=['POST'])
@login_required
def follow(username):
    # generate empty form to ensure data is passed
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot follow yourself!')
            return redirect(url_for('user', username=username))
        current_user.follow(user)
        db.session.commit()
        flash('You are following {}!'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))
@app.route('/unfollow/<username>', methods=['POST'])
@login_required
def unfollow(username):
    form = EmptyForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=username).first()
        if user is None:
            flash('User {} not found.'.format(username))
            return redirect(url_for('index'))
        if user == current_user:
            flash('You cannot unfollow yourself!')
            return redirect(url_for('user', username=username))
        current_user.unfollow(user)
        db.session.commit()
        flash('You are not following {}.'.format(username))
        return redirect(url_for('user', username=username))
    else:
        return redirect(url_for('index'))