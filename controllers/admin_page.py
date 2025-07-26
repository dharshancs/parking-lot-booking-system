from flask import Blueprint, render_template, redirect, url_for,session
from functools import wraps
from .__init__ import conn_database

admin_view = Blueprint('admin',__name__,url_prefix='/admin')


#decorator to check if admin is logged in before accessing the below routes


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session or session.get('is_admin') != True:
            return redirect(url_for('base.admin_login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_view.route('/home')
@admin_required
def admin_home():
    return 'admin home'

@admin_view.route('/users')
@admin_required
def user_management():
    return 'admin manages users here'

@admin_view.route('search')
@admin_required
def admin_search():
    return 'admin search page'

@admin_view.route('/summary')
@admin_required
def admin_summary():
    return 'admin summary'

@admin_view.route('/edit_profile')
@admin_required
def admin_profile():
    return 'admin profile'

@admin_view.route('logout')
@admin_required
def admin_logout():
    return 'admin logouts'

