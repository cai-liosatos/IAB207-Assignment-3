# Importing relevant packages
from flask import Blueprint, flash, render_template, request, url_for, redirect 
from werkzeug.security import generate_password_hash, check_password_hash
from .models import User
from .forms import LoginForm,RegisterForm
from flask_login import login_user, login_required, logout_user
from . import db


#create a blueprint
bp = Blueprint('auth', __name__)

# Define login function
@bp.route('/login', methods=['GET','POST'])
def login():
    login_form = LoginForm()
    error=None
    if(login_form.validate_on_submit()==True):
        #get the username and password from the form
        user_name = login_form.user_name.data
        password = login_form.password.data
        u1 = User.query.filter_by(username=user_name).first() # Compare user_name from form with the database
        #if there is no user with that name
        if u1 is None:
            error='Incorrect user name or password'
        elif not check_password_hash(u1.password_hash, password): # compares the password from the form and DB
            error='Incorrect user name or password'
        if error is None:
            login_user(u1)
            return redirect(url_for('main.index'))
        else:
            flash(error)
    return render_template('user.html', form=login_form, heading='Login')

# Define register function
@bp.route('/register', methods=['GET','POST'])
def register():
    register = RegisterForm()
    #the validation of form submis is fine
    if (register.validate_on_submit() == True):
            #get information from the form
            uname =register.user_name.data
            pwd = register.password.data
            email=register.email_id.data
            phNo=register.contact_number.data
            address=register.address.data
            #compare username of form with the DB
            u1 = User.query.filter_by(username=uname).first()
            if u1:
                flash('User name already exists, please login')
                return redirect(url_for('auth.login'))
            pwd_hash = generate_password_hash(pwd)
            #create a new user in DB
            new_user = User(username=uname, password_hash=pwd_hash, email=email, contact_number=phNo, address=address)
            db.session.add(new_user)
            db.session.commit()
            #commit to the database and prompt user to login
            flash('Successfully registered, please login to continue', 'success')
            return redirect(url_for('auth.login'))
    #the else is called when there is a get message
    else:
        return render_template('user.html', form=register, heading='Register')

# Define function for logging out
@bp.route('/logout')
@login_required
def logout():
    login_form = LoginForm()
    logout_user()
    flash('You have been logged out', 'warning') 
    return redirect(url_for('main.index'))
