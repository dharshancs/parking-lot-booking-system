from flask import Blueprint, render_template, request, flash, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
import sqlite3


u_view = Blueprint('user',__name__)

def conn_database():  #to connect to database for login and registration
    conection = sqlite3.connect('Parking.db')
    conection.row_factory = sqlite3.Row      #to convert tuple form to dictionary form
    return conection


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
            return redirect(url_for('user.user_register'))
        
        curr.execute('SELECT id from users WHERE email = ?',(email,))
        existing_user = curr.fetchone()

        if existing_user:
            #flash message to be imserted
            conn.close()
            return redirect(url_for('user.user_login'))
        
        curr.execute('INSERT INTO USERS (name,email,password) VALUES (?,?,?)',(name,email,generate_password_hash(password)))
        conn.commit()
        conn.close()

        return redirect(url_for('user.user_login'))
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
            return redirect(url_for('base.index'))
    return render_template('users/user_login.html')