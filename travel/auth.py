from flask import Blueprint, render_template, request, session, redirect, url_for, flash
from .forms import LoginForm, RegisterForm

bp = Blueprint('auth', __name__)

@bp.route('/login', methods=['GET', 'POST'])
def login():
    loginForm = LoginForm()
    if loginForm.validate_on_submit():
        print('Logged in user {}\nPassword: {}\n'.format(loginForm.user_name.data, loginForm.password.data), 'success')
        flash('You were successfully logged in', 'success')
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=loginForm, heading='Login')

@bp.route('/register', methods=['GET', 'POST'])
def register():
    registerForm = RegisterForm()
    if registerForm.validate_on_submit():
        print('Registered user {}\nEmail: {}\nPassword: {}\n'.format(registerForm.user_name.data, registerForm.password.data, registerForm.email_id.data))
        flash('You have successfully registered', 'success')
        return redirect(url_for('auth.login'))
    return render_template('user.html', form=registerForm, heading='Register')

# @mainbp.route('/logout')
# def logout():

