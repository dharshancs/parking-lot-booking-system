from flask import render_template,redirect, url_for,Blueprint,session,request
from .__init__ import conn_database
from werkzeug.security import generate_password_hash
from functools import wraps

user_view = Blueprint('user',__name__,url_prefix='/user')

#decorator function for login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('base.user_login'))
        return f(*args, **kwargs)
    return decorated_function



@user_view.route('/home')
@login_required
def user_home():
    return render_template('users/user_home.html')

@user_view.route('/summary')
@login_required
def user_summary():
    return render_template('users/user_summary.html')

@user_view.route('/edit_profile',methods=['POST','GET'])
@login_required
def user_profile():
    conn = conn_database()
    curr = conn.cursor()

    curr.execute('SELECT * FROM USERS WHERE email =?',(session['username'],))
    user = curr.fetchone()
    id = user['id']
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        address = request.form['address']
        pincode = request.form['pincode']
        password = request.form['password']

        conn = conn_database()
        curr = conn.cursor()

        query = 'UPDATE USERS SET name = ?, address = ?, pincode = ?, password =? WHERE id = ?'
        data = (name,address,pincode,generate_password_hash(password),id)

        curr.execute(query,data)
        conn.commit()
        conn.close()
        return redirect(url_for('user.user_profile'))
    
    return render_template('users/user_edit_profile.html',user = user)

@user_view.route('/logout')
@login_required
def user_logout():
    session.clear()
    return redirect(url_for('base.user_login'))
    
