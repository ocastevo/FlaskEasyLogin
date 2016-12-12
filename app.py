###############################################################################
###                              main app                                   ###
###############################################################################
import flask
import time
import json

from functions import send_email
from functions import allowed_file
from flask import session, render_template, url_for, redirect, abort
from Forms import LoginForm
from Forms import RegisterForm
from Forms import PassResetForm
from Forms import ReadyResetForm
from Forms import ConfirmEmailForm
from Forms import UploadScriptForm
from users_table import Users
from project_table import Project
from config import app
from config import bcrypt
from config import ts
from db import db

#Register page
@app.route('/register', methods = ['POST', 'GET'])
def register():
    if 'username' in session:
        return flask.redirect(flask.url_for( 'root' ))
    web_title = 'Register'
    form = RegisterForm()
    if form.validate_on_submit():
        pw = bcrypt.generate_password_hash(str( form.pw.data ))

        #insert new user details to database
        user_insert = Users(str( form.username.data ), str( form.email.data ), 
                str( form.first_name.data ), str( form.last_name.data ), pw , 
                str( form.user_code ), str( form.profile_img ), False)
        db.session.add(user_insert)
        db.session.commit()

        #generate email containing the confirmation link to confirm email
        subject = "Confirm your email"
        token = ts.dumps(str( form.email.data ), salt='email-confirm-key')

        confirm_url = url_for(
            'confirm_email',
            token=token,
            _external=True)

        html = render_template(
            'activate.html',
            confirm_url=confirm_url)

        send_email(str( form.email.data ), subject, html)

        #tell user an email has been sent
        return render_template('check_email.html', title =  web_title)

    return render_template('register.html', register_form = form, title = web_title )


#email confirmation page
@app.route('/confirm/<token>', methods = [ 'POST', 'GET' ])
def confirm_email(token):
    web_title = 'Confirm Email'
    try:
        email = ts.loads(token, salt="email-confirm-key", max_age=86400)
    except:
        abort(404)
    web_title = 'Confirm Email - Sharp'
    form = ConfirmEmailForm()
    if form.validate_on_submit():
        #update database 
        user_data = Users.query.filter(Users.email == email).first_or_404()

        user_data.email_confirmed = True
        
        db.session.add(user_data)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('confirm_email.html', register_form = form, token = token, title = web_title)

@app.route('/reset', methods=["GET", "POST"])
def reset():
    web_title = 'Reset Password'
    form = PassResetForm()
    if form.validate_on_submit():
        #send password reset link 
        subject = "Password reset requested"
        send_to_email = str( form.email.data )
        token = ts.dumps(send_to_email, salt='recover-key')

        recover_url = url_for(
            'reset_with_token',
            token=token,
            _external=True)

        html = render_template(
            'recover.html',
            recover_url = recover_url)

        send_email(basic_email, subject, html)
        return redirect(url_for('index'))

    return render_template('reset.html', reset_pw_form = form, title = web_title)

@app.route('/reset/<token>', methods=["GET", "POST"])
def reset_with_token(token):
    web_title = 'Reset Password'
    try:
        email = ts.loads(token, salt="recover-key", max_age=600)
    except:
        abort(404)

    form = ReadyResetForm()

    if form.validate_on_submit():
        #update database with new password
        user_reset = Users.query.filter(Users.email == email).first_or_404()

        user_reset.password = bcrypt.generate_password_hash(str( form.pw.data ))

        db.session.add(user_reset)
        db.session.commit()

        return redirect(url_for('login'))

    return render_template('reset_with_token.html', form = form, token = token, title = web_title)

@app.route('/login', methods=['GET', 'POST'])
def login():
    web_title = 'Login'
    if 'username' in session:
        return flask.redirect(flask.url_for( 'root' ))

    web_title = 'Login'
    form = LoginForm()
    form.validate_on_submit()

    if flask.request.method == 'GET':
        error_message = ''
        return render_template('login.html', failed_login = error_message, login_form = form, title = web_title)

    email = flask.request.form['email']
    login_results = Users.query.filter(Users.email == email, Users.email_confirmed == True).first()
    
    if login_results is not None:
        password = str( login_results.password )
        input_password = str( flask.request.form['pw'] )
        if bcrypt.check_password_hash(password, input_password):
            session['first_name'] = str(login_results.first_name)
            session['last_name'] = str(login_results.last_name)
            session['email'] = str(login_results.email)
            session['username'] = str(login_results.username)
            session['user_code'] = str(login_results.user_code)
            session['profile_img'] = str(login_results.profile_img)

            return flask.redirect(flask.url_for('root'))

    if len( form.errors ) > 0:
        error_message = ''
    else:
        error_message = 'Username or password incorrect.'

    return render_template('login.html', failed_login = error_message, login_form = form, title = web_title)


@app.route('/root')
def root():
    if 'username' not in session:
        return flask.redirect(flask.url_for( 'login' ))
    web_title = 'Root'
    return render_template('root.html', title = web_title)

@app.route('/logout')
def logout():
    if 'username' not in session:
        return flask.redirect(flask.url_for( 'login' ))
    for a in session.keys():
        session.pop(a)
    return flask.redirect(flask.url_for( 'index' ))

@app.route('/settings', methods = ['POST', 'GET'])
def settings():
    if 'username' not in session:
        return flask.redirect(flask.url_for( 'login' ))
    web_title = 'Settings'
    return render_template('settings.html', title = web_title)

@app.route('/')
def index():
    web_title = 'Home'
    return render_template('index.html', title = web_title)

if __name__ == '__main__':
    app.run(debug = True)
