from app import db
from flask import render_template, flash, redirect, url_for, request, current_app
from datetime import datetime
from flask_login import login_required
from app.models.user_model import Users
from app.user import bp




#------------USER PAGE--------------------------------------------------------------
@bp.route('/user/<username>')
@login_required    # view is protected by non-logged users
def user (username):
    """user main page, where all his post are shown

    :param username: the username of the user
    :type username: str
    """
    user = Users.query.filter_by(username = username).first_or_404() # this method returns a 404 error if user is null
    
    
    return render_template('user.html', user=user, title = user.username)