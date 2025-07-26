from flask import Blueprint, render_template, redirect, url_for,session,request
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

    return render_template('admin/admin_home.html')

@admin_view.route('/users')
@admin_required
def user_management():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM USERS')
    user_list = curr.fetchall()
    conn.close()

    return render_template('admin/admin_users.html',users = user_list)


@admin_view.route('search')
@admin_required
def admin_search():
    return render_template('admin/admin_search.html')

@admin_view.route('/summary')
@admin_required
def admin_summary():
    return render_template('admin/admin_summary.html')

@admin_view.route('/edit_profile',methods=['POST','GET'])
@admin_required
def admin_profile():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM ADMIN WHERE id = ?',(session['id'],))
    admin = curr.fetchone()
    conn.close()

    id = admin['id']
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        conn = conn_database()
        curr = conn.cursor()

        query = "UPDATE ADMIN SET username = ?, password = ? WHERE id =?"
        data = (username,password,id)

        curr.execute(query,data)
        conn.commit()
        conn.close()
        return redirect(url_for('admin.admin_profile'))
    
    return render_template('admin/admin_edit_profile.html',admin=admin)

@admin_view.route('logout')
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for('base.admin_login'))
    

