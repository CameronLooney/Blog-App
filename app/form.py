from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, SubmitField
from wtforms.validators import ValidationError, DataRequired, Email, EqualTo
from app.models import User
class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Remember Me')
    submit = SubmitField('Sign In')

class RegisterForm(FlaskForm):
    #form details
    username = StringField('Username', validators=[DataRequired()])
    # ensure email is a valid email format
    email = StringField('Email', validators=[DataRequired(),Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    # ensure passwords match
    password2 = PasswordField('Repeat Password', validators=[DataRequired(),EqualTo('password')])
    submit = SubmitField('Register')

    def validate_username(self,username):
        # query will return user if it exists, if user is true the name is taken
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("This username is already registered, please choose another.")

    def validate_email(self,username):
        user = User.query.filter_by(username = username.data).first()
        if user is not None:
            raise ValidationError("This email is already registered, please login or use another email.")