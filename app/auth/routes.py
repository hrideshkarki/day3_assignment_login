from flask import Blueprint, redirect, render_template, request, url_for
from .forms import LoginForm, SignUpForm
from ..models import User
from flask_login import login_user, logout_user, login_required

auth = Blueprint('auth', __name__, template_folder='auth_templates')

@auth.route('/')
def homePage():
    return render_template('home.html')

@auth.route('/signup', methods=["GET", "POST"])
def signupPage():
    form = SignUpForm()
    
    if request.method == 'POST':
        if form.validate():
            first_name = form.first_name.data
            last_name = form.last_name.data
            username = form.username.data
            email = form.email.data
            password = form.password.data

            # add user to database
            # if User exists:
            #     print(error msg)
            # else:
            user = User(first_name, last_name, username, email, password)
        
            user.saveToDB()
            account = {
                'first_name': first_name,
                'last_name': last_name,
                'username': username,
                'email': email
            }
        return render_template('signup.html', form = form, account=account)
    return render_template('signup.html', form = form)

@auth.route('/login', methods=["GET", "POST"])
def loginPage():
    form = LoginForm()
    if request.method == "POST":
        if form.validate():
            username = form.username.data
            password = form.password.data

            user = User.query.filter_by(username=username).first()            
            if user:
                # verify password
                if user.password == password:
                    login_user(user)
                    return redirect(url_for('homePage'))
                else:
                    print('invalid password')
            else:
                print('incorrect username or password')


    return render_template('login.html', form = form)

@auth.route('/logout')
@login_required
def logMeOut():
    logout_user()
    return redirect(url_for('loginPage'))