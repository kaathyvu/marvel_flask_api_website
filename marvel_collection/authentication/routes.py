from flask import Blueprint, render_template, request, redirect, url_for, flash
from marvel_collection.forms import UserSignInForm, UserSignUpForm
from marvel_collection.models import User, db
from werkzeug.security import check_password_hash
from flask_login import login_user, logout_user, login_required


auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/sign-in', methods=['GET', 'POST'])
def signin():
    signinform = UserSignInForm()
    try:
        if request.method=='POST' and signinform.validate_on_submit():
            email = signinform.email.data
            password = signinform.password.data

            logged_user = User.query.filter(User.email == email).first()
            if logged_user and check_password_hash(logged_user.password, password):
                login_user(logged_user)
                user_first_name = logged_user.first_name
                flash(f"You have successfully logged in, {user_first_name}!", "auth-success")
                return redirect(url_for('site.profile'))
            else:
                flash(f"Incorrect Email and/or Password. Please try again.", "auth-failed")
                return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid form data. Please try again")
    return render_template('signin.html', signinform=signinform)

@auth.route('/sign-up', methods=['GET', 'POST'])
def signup():
    signupform = UserSignUpForm()
    try:
        if request.method=="POST" and signupform.validate_on_submit():
            email = signupform.email.data
            first_name = signupform.first_name.data
            last_name = signupform.last_name.data
            password = signupform.password.data

            user = User(email=email, first_name=first_name, last_name=last_name, password=password)
            db.session.add(user)
            db.session.commit()

            flash(f"You have successfully joined the Marvel Universe, {first_name}!", "user-created")
            return redirect(url_for('auth.signin'))
    except:
        raise Exception("Invalid form data. Please check your form.")

    return render_template('signup.html', signupform=signupform)

@auth.route('/log-out')
@login_required
def logout():
    logout_user()
    flash(f"You have logged out", "logged-out")
    return redirect(url_for('site.home'))