# anything that's not related to authentication will be placed in this file

from flask import Blueprint, render_template, request,flash, redirect,url_for
from .models import User
from . import db
from flask_login import login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash

# file is a blueprint of our application
auth = Blueprint('auth', __name__)


# defining a view/route
# by default, only can accept get requests but now can accept both
@auth.route('/login', methods=["GET", "POST"])
def login(): # function will run everytime we go this '/' route
    if request.method=='POST':
        email = request.form.get('email')
        password = request.form.get('password')

        #query in db is user is in db/ is valid
        user = User.query.filter_by(email=email).first()
        # found the user and checkin the password
        if user:
            if check_password_hash(user.password, password):
                flash("Logged in successfully!", category='success')

                # remembers user is logged in unless user clears browsing
                login_user(user, remember=True)
                return redirect(url_for('views.home'))
            else:
                flash("Incorrect password. Try again!", category='error')
        else:
            flash("Email does not exist.", category='error')

    
    # get informattion that was sent in this form
    data = request.form
    print(data)

    # can pass eg. text variable to our login.html template
    return render_template("login.html", user=current_user)

@auth.route('/logout')
@login_required #make sure cannot access this route unless user is logged in
def logout(): # function will run everytime we go this '/' route
    logout_user()
    return redirect(url_for('auth.login'))

@auth.route('/sign-up', methods=["GET", "POST"])
def sign_up(): # function will run everytime we go this '/' route
    if request.method == 'POST':
        email = request.form.get('email')
        first_name = request.form.get('firstName')
        password1 = request.form.get('password1')
        password2 = request.form.get('password2')

        #query in db is user is in db/ is valid
        user = User.query.filter_by(email=email).first()
        if user:
            flash('Email already exists', category='error')

        if len(email) < 4:
            flash('Email must be greater than 3 characters.', category='error')
        elif len(first_name) < 2:
            flash('First Name must be greater than 1 characters.', category='error')
        elif password1 != password2:
            flash("Passwords don\'t match.", category='error')
        elif len(password1) < 7:
            flash('Password must be at least 7 characters.', category='error')
        else:
            # add user to db
            new_user = User(email=email, first_name=first_name, password=generate_password_hash(password1, method="sha256"))
            db.session.add(new_user)
            db.session.commit()
            login_user(user, remember=True)
            flash("Account created!", category='success')
            return redirect(url_for('views.home'))

    return render_template("sign_up.html", user=current_user)