from flask import Blueprint, render_template, redirect, url_for,session,request
from functools import wraps
from .__init__ import conn_database

admin_view = Blueprint('admin',__name__,url_prefix='/admin')


#decorator to check if admin is logged in before accessing the below routes


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session or session.get('is_admin') != True:
            return redirect(url_for('base.user_login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_view.route('/home',methods = ['POST','GET'])
@admin_required
def admin_home():
    if request.method == 'POST':
        prime_location = request.form['prime_location']
        address = request.form['address']
        pincode = request.form['pincode']
        price = request.form['price']
        max_no_of_spots = request.form['max_no_of_spots']

        conn = conn_database()
        curr = conn.cursor()

        curr.execute('INSERT INTO PARKING_LOT (prime_location,price ,address,pincode,max_no_of_spots) VALUES (?,?,?,?,?)',(prime_location,price,address,pincode,max_no_of_spots))
        id = curr.lastrowid
        for i in range(1,int(max_no_of_spots)+1):
            spot_name = f"{prime_location} Spot # {i}"
            curr.execute('INSERT INTO PARKING_SPOT (lot_id,slot_number,status) VALUES (?,?,?)',(id,spot_name,"A"))
        conn.commit()
        conn.close()
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM PARKING_LOT')
    lots = curr.fetchall()
    i=0
    spots = []
    for lot in lots:
        curr.execute('SELECT * FROM PARKING_SPOT WHERE lot_id =?',(lot['id'],))
        spots.append(curr.fetchall())
        i+=1
        

    return render_template('admin/admin_home.html',lots=lots, spots=spots)

@admin_view.route('/users')
@admin_required
def user_management():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM USERS WHERE id!=0')
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
    curr.execute('SELECT * FROM USERS WHERE id = ?',(session['id'],))
    admin = curr.fetchone()
    print(session['id'])
    print(admin)
    conn.close()

    id = admin['id']
    
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        conn = conn_database()
        curr = conn.cursor()

        query = "UPDATE USERS SET email = ?, password = ? WHERE id =?"
        data = (email,password,id)

        curr.execute(query,data)
        conn.commit()
        conn.close()
        return redirect(url_for('admin.admin_profile'))
    
    return render_template('admin/admin_edit_profile.html',admin=admin)

@admin_view.route('logout')
@admin_required
def admin_logout():
    session.clear()
    return redirect(url_for('base.user_login'))
    

