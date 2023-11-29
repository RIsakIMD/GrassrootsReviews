import re
from flask import render_template, request, redirect, flash, session
from flask_app import app
from flask_app.models.user import User

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/account')
def account():
    if session.get('user') == None:
        return redirect('/login')

    return render_template('account.html', user=User.get_user(session['user']))

@app.route('/submit_registration', methods=['POST'])
def submit_registration():
    success = True

    if len(request.form['name']) < 2:
        success = False
        flash("Name must be longer than 2")

    if not EMAIL_REGEX.match(request.form['email']):
        success = False
        flash("Invalid email")

    if len(request.form['password1']) < 8:
        success = False
        flash("Password must be longer than 8")

    if request.form['password1'] != request.form['password2']:
        success = False
        flash("Password confirmation does not match")

    if success:
        session['user'] = User.add_user(request.form)
        return redirect('/account')

    return redirect('/login')


@app.route('/submit_login', methods=['POST'])
def submit_login():
    success = True

    if not EMAIL_REGEX.match(request.form['email']):
        success = False
        flash("Invalid email")

    if len(request.form['password1']) < 8:
        success = False
        flash("Password must be longer than 8")

    result = User.get_user_id(request.form)

    if result == None:
        success = False
        flash("Invalid email/password")

    if success:
        session['user'] = result.id
        return redirect('/account')

    return redirect('/login')

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')

