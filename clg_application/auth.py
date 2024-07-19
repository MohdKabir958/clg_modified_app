from flask import Blueprint, render_template, redirect, url_for, request, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import login_user, logout_user, login_required,current_user
auth = Blueprint('auth', __name__)

@auth.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        remember = request.form.get('remember')
        remember = True if remember else False
        from . models import User
        user = User.query.filter_by(email=email).first()
        if user and check_password_hash(user.password,password=password):
            login_user(user=user,remember=remember) 
            flash("Login Successfull!", 'success')
            return redirect(url_for("main.account"))
        else:
            flash("Invalid Email or password  ",'failure')
    return render_template("login2.html")
        

@auth.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        fname = request.form['fname']
        lname = request.form['lname']
        name = fname + ' ' + lname
        email = request.form["email"]
        password = request.form["password"]
        confirm_password = request.form["confirm_password"]
        hashed_password = generate_password_hash(password=password,method='pbkdf2:sha256')


        if password != confirm_password:
            flash("Passwords don't match", "error")
            return redirect(url_for("auth.signup"))
        from .models import User
        from . import db 
        existing_user = User.query.filter_by(email=email).first()
        if existing_user:
            flash(f"User with {email} already exits!")
            return render_template("signup.html")
        new_user = User(name=name, email=email, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash("Signup Successful!", 'success')
        return redirect(url_for("auth.login"))
    
    # Handle GET request: render the signup page
    return render_template('signup2.html')

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.index'))

 

