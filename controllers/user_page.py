from flask import render_template,redirect, url_for,Blueprint,session,request,flash
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
            flash("You need to login to access this page","danger")
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
            available_slot_data.append((lot['id'], available_spot['spot_number']))
        else:
            available_slot_data.append((lot['id'], "No Available Slot"))


    conn.close()
    conn=conn_database()
    curr=conn.cursor()
    curr.execute('''SELECT BD.price as paid_price,PS.lot_id as li,BD.spot_number as sn,BD.id as id,BD.vehicle_number as vn,BD.timestamp_booked as tb,PL.prime_location as pl,BD.timestamp_released as tr,PL.price as price,BD.booking_status as b_status
                 FROM BOOKING_DETAILS BD 
                 JOIN  PARKING_SPOT PS ON PS.spot_number=BD.spot_number AND PS.lot_id = BD.lot_id
                 JOIN  PARKING_LOT PL on PL.id=PS.lot_id WHERE BD.user_id=? ORDER BY BD.timestamp_booked DESC''',(session['id'],))
    booking_details = curr.fetchall()
    conn.close()
    flag = True

    if request.method == 'POST':
        request_name = request.form['form_type']
        
        if request_name == 'book_lot':
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('SELECT no_of_available FROM PARKING_LOT WHERE id =?',(request.form['lot_id'],))
            available = int(curr.fetchone()[0])
            if available < 1:
                flash("No Slots available to Book","danger")
                return(redirect(url_for('user.user_home')))
            curr.execute('INSERT INTO BOOKING_DETAILS (user_id,lot_id,spot_number,timestamp_booked,vehicle_number,booking_status) VALUES(?,?,?,?,?,?)',(session['id'],request.form['lot_id'],request.form['spot_number'],int(datetime.now().timestamp()),request.form['vehicle_number'],"open"))
            conn.commit()
            curr.execute('UPDATE PARKING_SPOT SET status ="O" WHERE lot_id = ? AND spot_number=?',(request.form['lot_id'],request.form['spot_number']))
            curr.execute('UPDATE PARKING_LOT SET no_of_available=no_of_available-1 where id=?',(request.form['lot_id'],))
            conn.commit()
            conn.close()
            return redirect(url_for('user.user_home'))
        if request_name == 'release_spot':
            spot_number = request.form['spot_number']
            release_time_str =request.form['release_time']
            dt_obj = datetime.strptime(release_time_str, "%d-%m-%Y %H:%M:%S")
            release_time_unix = int(dt_obj.timestamp())
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('UPDATE BOOKING_DETAILS SET booking_status = ?,timestamp_released=?,price =? WHERE lot_id = ? AND spot_number =? ' ,("closed",release_time_unix,request.form['total_cost'],request.form['lot_id'],spot_number))
            conn.commit()
            curr.execute('UPDATE PARKING_SPOT SET status =? WHERE lot_id = ? AND spot_number = ?',('A',request.form['lot_id'],spot_number))
            curr.execute('UPDATE PARKING_LOT SET no_of_available=no_of_available+1 where id=?',(request.form['lot_id'],))
            conn.commit()
            conn.close()
            flash("Parking Spot Released","success")
            return redirect(url_for('user.user_home'))            
        if request_name == 'search_parking':
            conn = conn_database()
            curr = conn.cursor()
            prime_location = request.form ['prime_location']
            curr.execute('SELECT * FROM PARKING_LOT WHERE prime_location LIKE ? OR pincode LIKE ?',('%' + prime_location + '%','%' + prime_location + '%'))
            flag = False
            if not prime_location or prime_location.strip() =="":
                curr.execute('SELECT * FROM PARKING_LOT')
                flag = True
            
            parking_lots = curr.fetchall()
            return render_template('users/user_home.html',parking_lots = parking_lots,booking_details = booking_details,available_slot_data=available_slot_data,datetime=datetime,flag = flag)
    return render_template('users/user_home.html',parking_lots = parking_lots,booking_details = booking_details,available_slot_data=available_slot_data,datetime=datetime,flag = flag)

@user_view.route('/summary')
@login_required
def user_summary():

    user_id = session['id']
    conn = conn_database()
    curr = conn.cursor()

    curr.execute("SELECT * FROM USERS WHERE id=?", (session['id'],))
    user = curr.fetchone()

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE user_id=?", (user_id,))
    total_bookings = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE user_id=? AND booking_status='open'", (session['id'],))
    active_bookings = curr.fetchone()[0]

    curr.execute("SELECT SUM(price) FROM BOOKING_DETAILS WHERE user_id=? AND booking_status='closed'", (session['id'],))
    total_spent = curr.fetchone()[0] or 0

    curr.execute('''SELECT B.*, P.lot_id 
                    FROM BOOKING_DETAILS B 
                    JOIN PARKING_SPOT P ON B.spot_number = P.spot_number AND B.lot_id=P.lot_id
                    WHERE B.user_id=?
                    ORDER BY B.timestamp_booked DESC 
                    LIMIT 10''', (session['id'],))
    recent_bookings = curr.fetchall()

    return render_template('users/user_summary.html', user=user, total_bookings=total_bookings,
                           active_bookings=active_bookings, total_spent=total_spent,
                           recent_bookings=recent_bookings,datetime=datetime)


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
        conn = conn_database()
        curr = conn.cursor()

        query = 'UPDATE USERS SET name = ?, address = ?, pincode = ?  WHERE id = ?'
        data = (name,address,pincode,id)

        curr.execute(query,data)
        conn.commit()
        conn.close()
        flash("Profile Updated Successfully","success")
        return redirect(url_for('user.user_profile'))
    
    return render_template('users/user_edit_profile.html',user = user)

@user_view.route('/logout')
@login_required
def user_logout():
    session.clear()
    flash("Profile Updated Successfully","success")
    return redirect(url_for('base.user_login'))
    
