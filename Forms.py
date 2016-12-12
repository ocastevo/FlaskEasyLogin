from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextField, SubmitField, FileField
from wtforms.validators import InputRequired, Email, EqualTo, Length, Regexp, DataRequired
from form_checks import user_email
from functions import genString

password_regex = '^(?=.*?\d)(?=.*?[A-Z])(?=.*?[a-z])[A-Za-z\d]{10,}$'
regexp_message = 'Must contain:' + \
'<ul>' + \
    '<li>Atleast one digit</li>' + \
    '<li>Atleast one uppercase</li> '+ \
    '<li>Atleast one lowercase</li>'+ \
'</ul>'

class LoginForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email()], render_kw = { "placeholder": "Email"})
    pw = PasswordField('pw', validators = [InputRequired()], render_kw = { "placeholder": "Password"})

class RegisterForm(FlaskForm):
    username = StringField('username', validators = [InputRequired(), 
        Length(min = 5, max = 40)], render_kw = { "placeholder": "Username"})
    first_name = StringField('first_name', validators = [InputRequired(), 
        Length(min = 3, max = 30)], render_kw = { "placeholder": "First Name"})
    last_name = StringField('last_name', validators = [InputRequired(), 
        Length(min = 3, max = 30)], render_kw = { "placeholder": "Last Name"})

    email = StringField('email', validators = [InputRequired(), Email(), 
        Length(min = 5, max = 50), user_email], render_kw = { "placeholder": "Email"})
    confirm_email = StringField('confirm_email', validators = [InputRequired(), 
        Email(), EqualTo('email', message = 'Emails don\'t match.'), 
        Length(min = 5, max = 50)], render_kw = { "placeholder": "Confirm Email"})


    pw = PasswordField('pw', validators = [InputRequired(), Length(min = 10), 
        Regexp(password_regex, message = regexp_message)], render_kw = { "placeholder": "Password"})
    confirm_pw = PasswordField('confirm_pw', validators = [InputRequired(), EqualTo('pw', 
        message = 'Passwords don\'t match.'), Length(min = 10)], render_kw = { "placeholder": "Confirm Password"})

    user_code = genString(30)
    profile_img = 'profile_imgs/default.jpg'

class PassResetForm(FlaskForm):
    email = StringField('email', validators = [InputRequired(), Email()], render_kw = { "placeholder": "Email"})

class ReadyResetForm(FlaskForm):
    pw = PasswordField('pw', validators = [InputRequired(), Length(min = 10), 
        Regexp(password_regex, message = regexp_message)], render_kw = { "placeholder": "Password"})
    confirm_pw = PasswordField('confirm_pw', validators = [InputRequired(), EqualTo('pw', 
        message = 'Passwords don\'t match.'), Length(min = 10)], render_kw = { "placeholder": "Confirm Password"})

class ConfirmEmailForm(FlaskForm):
    confirm = SubmitField('confirm_email', validators = [InputRequired()], render_kw = { "value" : "Confirm Email", "class": "button button-primary" })
