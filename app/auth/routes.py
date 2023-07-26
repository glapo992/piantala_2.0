from app.extensions import db
from flask import render_template, flash, redirect, url_for, request
from flask_login import current_user, login_user, logout_user
from werkzeug.urls import url_parse
from app.auth.forms import LoginForm, RegistrationForm
from app.models import Users
from app.auth import bp


@bp.route('/login', methods=['GET', 'POST']) 
def login():
    """ this view manage the login function 
    the login library has required items that can be used 
    - is_authenticated: a property that is True if the user has valid credentials or False otherwise.
    - is_active: a property that is True if the user's account is active or False otherwise.
    - is_anonymous: a property that is False for regular users, and True for a special, anonymous user.
    - get_id(): a method that returns a unique identifier for the user as a string (unicode, if using Python)
    """
    if current_user.is_authenticated:
        return redirect (url_for('plantnet.index'))                      #  if the user is already auth, just return the index
     
    form = LoginForm()
    if form.validate_on_submit():                               # procss the form, returns true or false depending on the validators. if false require an error handler
        user = Users.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash('username o password errati')                    # must be handled in html. did in base.html so all pages can handle flash messages
            return redirect(url_for('auth.login'))                   # redirect with the url_for method
        login_user(user=user, remember=form.remember_me.data)   #flask function register the user as logged in. sets a variable current_user with the logged one for the duration of the session
        next_page = request.args.get('next')                    # the argument of the request -> is the url to the page the user want to visit, caught by @login_required (.../login?next=%2Ffeed)
        
        if not next_page or url_parse(next_page).netloc != "":  
            # ensure that the next is on the same site 
            #(an attacker could insert a different url in the ?next and have the login token to acceed also if is on another site). 
            #to determne if the url is relative or not, the netloc component must exist
            next_page = (url_for('plantnet.index'))  # if next page does not exist, the url for index is assigned
        return redirect (next_page)

    return render_template ('login.html', form = form, title = 'Accedi')

@bp.route('/logout')
def logout():
    """logs out the already logged user """
    logout_user()
    return redirect(url_for('plantnet.index'))


@bp.route('/registration', methods=['GET', 'POST']) # this method accepts also post requests, as specified in the html from 
def registration():
    """ new user registration view """
    if current_user.is_authenticated:
        return redirect (url_for('plantnet.index'))    
    form = RegistrationForm()
    if form.validate_on_submit():
        user = Users(username = form.username.data, email = form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash('registrazione avvenuta con successo')
        return redirect(url_for('auth.login'))
    return render_template('registration.html', form = form , title= 'Registrazione')   