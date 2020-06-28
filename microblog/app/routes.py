from flask import render_template, redirect,flash, url_for,  request
from app import app, db
from app.forms import LoginForm, RegistrationForm
from flask_login import current_user, login_user, logout_user,login_required
from app.models import User
from werkzeug.urls import url_parse


@app.route('/')
@app.route('/index')
@login_required
def index():
    
    posts = [
        {
            'author': {'username': 'John'},
            'body': 'Beautiful day in Portland!'
        },
        {
            'author': {'username': 'Susan'},
            'body': 'The Avengers movie was so cool!'
        }
    ]
    return render_template('index.html', title='Home', posts=posts)

@app.route('/login', methods=['GET', 'POST'])
def login():
    #check if user is authenticated already, redirect to index page if they are
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()

    #check if the all required form fields are provided, proceed to validate user details if they are
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('invalid username or password')
            return redirect(url_for('login'))

        #set currently logged in user details for flask_login extention to handle    
        login_user(user, remember=form.remember_me.data)

        #check if there was a page the user tried to access prior to logging in
        next_page = request.args.get('next')

        #ensure the next page is on the same site, else give them index page
        if not next_page or url_parse(next_page).netloc != '':
            return redirect(url_for('index'))

        return redirect(next_page)
    return render_template('login.html', form=form, title='Sign In')    

@app.route('/logout')
def logout():
     logout_user()
     return redirect(url_for('index'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('Congratulations, you are now a registered user!')
        return redirect(url_for('login'))
    return render_template('register.html', title='Register', form=form)     