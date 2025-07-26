from flask import render_template,redirect, url_for,Blueprint,session
from .__init__ import conn_database
from functools import wraps

user_view = Blueprint('user',__name__,url_prefix='/user')

#decorator function for login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if id not in session or session['is_admin'] == True:
            return redirect(url_for('base.user_login'))
        return f(*args, **kwargs)
    return decorated_function



@user_view.route('/home')
@login_required
def user_home():
    return '<h1>Welcome home user<h1>'

@user_view.route('/summary')
@login_required
def user_summary():
    return 'This is summary page'

@user_view.route('/edit_profile')
@login_required
def user_profile():
    return 'Edit user profile page'

@user_view.route('/logout')
@login_required
def user_logout():
    return 'logout done'
