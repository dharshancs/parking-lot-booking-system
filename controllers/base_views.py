from flask import Blueprint, render_template, request, flash, redirect, url_for, session
from werkzeug.security import generate_password_hash, check_password_hash
from .__init__ import conn_database


u_view = Blueprint('base',__name__)



@u_view.route('/')
def index():
    return render_template('index.html')

@u_view.route('/register', methods=['POST','GET'])
def user_register():
    if request.method == 'POST':
        name = request.form['user_name']
        email = request.form['user_email']
        password = request.form['user_password']
        confirm_password = request.form['user_confirm_password']
        
        conn = conn_database()
        curr = conn.cursor()

        if not(password == confirm_password):
            #flash message to be imserted
            conn.close()
            return redirect(url_for('base.user_register'))
        
        curr.execute('SELECT id from users WHERE email = ?',(email,))
        existing_user = curr.fetchone()

        if existing_user:
            #flash message to be imserted
            conn.close()
            return redirect(url_for('base.user_login'))
        
        curr.execute('INSERT INTO USERS (name,email,password) VALUES (?,?,?)',(name,email,generate_password_hash(password)))
        conn.commit()
        conn.close()

        return redirect(url_for('base.user_login'))
    return render_template('users/user_register.html')

@u_view.route('/login',methods=['POST','GET'])
def user_login():
    if request.method == 'POST':
        email = request.form['user_email']
        password = request.form['user_password']

        conn = conn_database()
        curr = conn.cursor()

        curr.execute('SELECT * FROM USERS WHERE email=?',(email,))
        user=curr.fetchone()
        conn.close()

        #Add check for wrong password or no user

        if user and check_password_hash(user['password'],password):
            if not user['is_admin']:
                session['id'] = user['id']
                session['email'] = user['email']
                session['is_admin'] = False
                return redirect(url_for('user.user_home'))
            elif user['is_admin']:
                session['id'] = user['id']
                session['email'] = user['email']
                session['is_admin'] = True
                return redirect(url_for('admin.admin_home'))
    return render_template('users/user_login.html')

