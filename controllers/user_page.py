from flask import render_template,redirect, url_for,Blueprint,session,request
from .__init__ import conn_database
from werkzeug.security import generate_password_hash
from functools import wraps
from datetime import datetime

user_view = Blueprint('user',__name__,url_prefix='/user')

#decorator function for login
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session:
            return redirect(url_for('base.user_login'))
        return f(*args, **kwargs)
    return decorated_function



@user_view.route('/home',methods = ['POST','GET'])
@login_required
def user_home():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM PARKING_LOT')
    parking_lots = curr.fetchall()
    available_slot_data = []
    for lot in parking_lots:
        curr.execute("SELECT * FROM PARKING_SPOT WHERE lot_id = ? AND status = 'A' LIMIT 1",(lot['id'],))
        available_spot = curr.fetchone()
        if available_spot:
            available_slot_data.append((lot['id'], available_spot['slot_number']))
        else:
            available_slot_data.append((lot['id'], "No Available Slot"))


    conn.close()
    conn=conn_database()
    curr=conn.cursor()
    curr.execute('''SELECT BD.slot_number as sn,BD.id as id,BD.vehicle_number as vn,BD.timestamp_booked as tb,PL.prime_location as pl,BD.timestamp_released as tr,PL.price as price,BD.booking_status as b_status
                 FROM BOOKING_DETAILS BD 
                 JOIN  PARKING_SPOT PS ON PS.slot_number=BD.slot_number 
                 JOIN  PARKING_LOT PL on PL.id=PS.lot_id WHERE BD.user_id=? ORDER BY BD.timestamp_booked DESC''',(session['id'],))
    booking_details = curr.fetchall()
    conn.close()

    if request.method == 'POST':
        request_name = request.form['form_type']
        
        if request_name == 'book_lot':
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('INSERT INTO BOOKING_DETAILS (user_id,slot_number,timestamp_booked,vehicle_number,booking_status) VALUES(?,?,?,?,?)',(session['id'],request.form['spot_id'],int(datetime.now().timestamp()),request.form['vehicle_number'],"OPEN"))
            conn.commit()
            curr.execute('UPDATE PARKING_SPOT SET status ="O" WHERE slot_number=?',(request.form['spot_id'],))
            conn.commit()
            conn.close()
            return redirect(url_for('user.user_home'))
        if request_name == 'release_spot':
            spot_id = request.form['spot_id']
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('UPDATE BOOKING_DETAILS SET booking_status = ? WHERE slot_number =?' ,("closed",spot_id))
            conn.commit()
            curr.execute('UPDATE PARKING_SPOT SET status =? WHERE slot_number = ?',('A',spot_id))
            conn.commit()
            conn.close()
            return redirect(url_for('user.user_home'))
        if request_name == 'search_parking':
            conn = conn_database()
            curr = conn.cursor()
            location_name = request.form ['location_name']
            curr.execute('SELECT * FROM PARKING_LOT WHERE prime_location = ?',(location_name,))
            flag = False
            if not location_name or location_name.strip() =="":
                curr.execute('SELECT * FROM PARKING_LOT')
                flag = True
            
            parking_lots = curr.fetchall()
            return render_template('users/user_home.html',parking_lots = parking_lots,booking_details = booking_details,available_slot_data=available_slot_data,datetime=datetime,flag = flag)

    
    return render_template('users/user_home.html',parking_lots = parking_lots,booking_details = booking_details,available_slot_data=available_slot_data,datetime=datetime)

@user_view.route('/summary')
@login_required
def user_summary():
    return render_template('users/user_summary.html')

@user_view.route('/edit_profile',methods=['POST','GET'])
@login_required
def user_profile():
    conn = conn_database()
    curr = conn.cursor()

    curr.execute('SELECT * FROM USERS WHERE email =?',(session['email'],))
    user = curr.fetchone()
    id = user['id']
    conn.close()

    if request.method == 'POST':
        name = request.form['name']
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
    
