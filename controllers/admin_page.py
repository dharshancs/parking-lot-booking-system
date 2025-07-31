from flask import Blueprint, render_template, redirect, url_for,session,request,flash
from functools import wraps
from .__init__ import conn_database




admin_view = Blueprint('admin',__name__,url_prefix='/admin')


#decorator to check if admin is logged in before accessing the below routes


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'id' not in session or session.get('is_admin') != True:
            flash("You need Admin Access to access the page","danger")
            return redirect(url_for('base.user_login'))
        return f(*args, **kwargs)
    return decorated_function


@admin_view.route('/home',methods = ['POST','GET'])
@admin_required
def admin_home():
    if request.method == 'POST':
        request_name = request.form['form_type']
        if request_name == "create_lot" :
            prime_location = request.form['prime_location']
            address = request.form['address']
            pincode = request.form['pincode']
            price = request.form['price']
            max_no_of_spots = request.form['max_no_of_spots']
            if int(max_no_of_spots) < 1:
                flash("Number of Spots must be Greater than 0","danger")
                return(redirect(url_for('admin.admin_home')))
            conn = conn_database()
            curr = conn.cursor()

            curr.execute('INSERT INTO PARKING_LOT (prime_location,price ,address,pincode,max_no_of_spots,no_of_available) VALUES (?,?,?,?,?,?)',(prime_location,price,address,pincode,max_no_of_spots,max_no_of_spots))
            id = curr.lastrowid
            for i in range(1,int(max_no_of_spots)+1):
                spot_name = f"{prime_location} Spot # {i}"
                curr.execute('INSERT INTO PARKING_SPOT (lot_id,spot_number,status) VALUES (?,?,?)',(id,spot_name,"A"))
            conn.commit()
            conn.close()
            flash("Lot Created","success")
            return redirect(url_for('admin.admin_home'))
        if request_name == 'delete_spot':
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('DELETE FROM PARKING_SPOT WHERE spot_number = ? AND lot_id = ?', (request.form['spot_number'], request.form['lot_id']))
            curr.execute('UPDATE PARKING_LOT SET max_no_of_spots= max_no_of_spots - 1, no_of_available=no_of_available-1 WHERE id = ?',(request.form['lot_id'],))

            conn.commit()
            conn.close()
            flash("Spot Deleted","success")
            return redirect(url_for('admin.admin_home'))
        if request_name == 'delete_lot':
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('SELECT COUNT(*) FROM PARKING_SPOT WHERE lot_id = ? and status ="O"',(request.form['lot_id'],))
            no_occupied = int(curr.fetchone()[0])
            if no_occupied == 0:
                curr.execute('DELETE FROM PARKING_LOT WHERE id=?',(request.form['lot_id'],))
                conn.commit()
                conn.close()
                flash("Lot Deleted","success")
                return(redirect(url_for('admin.admin_home')))
            else:
                flash("Cannot Delete Lots with Occupied Spots","danger")
                conn.close()
        if request_name == "edit_lot" :
            prime_location = request.form['prime_location']
            address = request.form['address']
            pincode = request.form['pincode']
            price = request.form['price']
            max_no_of_spots = int(request.form['max_no_of_spots'])
            lot_id = request.form['lot_id']
            conn = conn_database()
            curr = conn.cursor()
            curr.execute('SELECT COUNT(*) FROM PARKING_SPOT WHERE lot_id = ?',(lot_id,))
            previous_total_spots = int(curr.fetchone()[0])
            curr.execute('SELECT COUNT(*) FROM PARKING_SPOT WHERE lot_id = ? and status ="O"',(lot_id,))
            no_occupied = int(curr.fetchone()[0])
            if max_no_of_spots< 0:
                flash("Number of Spots cannot be Negative.", "danger")
                conn.close()
                return redirect(url_for('admin.admin_home'))
            if no_occupied == 0 and max_no_of_spots ==0:
                curr.execute('DELETE FROM PARKING_LOT WHERE id =?',(lot_id,))
                conn.close()
                flash("Lot Deleted since all Spots removed","success")
                return redirect(url_for('admin.admin_home'))
            if max_no_of_spots< no_occupied:
                flash("Number of Spots cannot be less than currently Occupied Spots.", "error")
                conn.close()
                return redirect(url_for('admin.admin_home'))
            curr.execute('UPDATE PARKING_LOT SET prime_location=?,price=?,address=?,pincode=?,max_no_of_spots=?, no_of_available = ? WHERE id =?',(prime_location,price,address,pincode,max_no_of_spots,max_no_of_spots-no_occupied,lot_id))
            if max_no_of_spots < previous_total_spots:
                spots_to_remove = previous_total_spots - max_no_of_spots
                curr.execute('''
                    SELECT id FROM PARKING_SPOT 
                    WHERE lot_id = ? AND status = 'A' 
                    ORDER BY CAST(SUBSTR(spot_number, INSTR(spot_number, '-') + 1) AS INTEGER) DESC 
                    LIMIT ?
                ''', (lot_id, spots_to_remove))
                removable_spot_ids = curr.fetchall()

                for spot_id in removable_spot_ids:
                    curr.execute('DELETE FROM PARKING_SPOT WHERE id = ?', (spot_id[0],))
                conn.commit()
                flash("Lot Updated","success")
                conn.close()
                return redirect(url_for('admin.admin_home'))
            elif max_no_of_spots>=previous_total_spots:
                for i in range(max_no_of_spots-previous_total_spots):
                    j = previous_total_spots
                    spot_name = f"{prime_location} Spot # {j}"
                    curr.execute('INSERT INTO PARKING_SPOT (lot_id,spot_number,status) VALUES (?,?,?)',(lot_id,spot_name,'A'))
                conn.commit()
                flash("Lot Updated","success")
                conn.close()
        return(redirect(url_for('admin.admin_home')))
    conn=conn_database()
    curr=conn.cursor()
    curr.execute('SELECT * FROM PARKING_LOT')
    lots = curr.fetchall()
    spots=[]
    for lot in lots:
        curr.execute('SELECT PS.id,PS.lot_id,PS.spot_number,PS.status,BD.id as bid,BD.user_id as email,BD.spot_number as sn,BD.timestamp_booked as tb,BD.vehicle_number as VN FROM PARKING_SPOT PS LEFT JOIN (SELECT * FROM BOOKING_DETAILS WHERE booking_status ="open" GROUP BY lot_id,spot_number) AS BD ON BD.spot_number = PS.spot_number AND BD.lot_id = PS.lot_id WHERE PS.lot_id =?',(lot['id'],))
        spots.append(curr.fetchall())
    conn.close()
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


@admin_view.route('search',methods=['GET','POST'])
@admin_required
def admin_search():
    results = None
    columns = []
    if request.method =='POST':
        field = request.form['field']
        value = request.form['value']
        conn=conn_database()
        curr=conn.cursor()
        if field == 'email':
            curr.execute(f"SELECT U.id as 'User ID',U.email as 'Email Address',U.name as 'Name',U.address as 'Address',U.pincode as 'Pincode',COUNT(CASE WHEN B.booking_status ='open' THEN 1 END) AS 'No of Active Bookings', COUNT(CASE WHEN B.booking_status ='closed' THEN 1 END) AS 'No of Past Bookings' FROM USERS U LEFT JOIN BOOKING_DETAILS B ON U.id = B.user_id WHERE {field} LIKE ? GROUP BY U.id,U.email,U.name,U.address",('%'+value+'%',))
        if field == 'prime_location':
            curr.execute(f"SELECT P.id as 'Parking Lot ID',P.prime_Location as 'Lot Prime Location Name',P.address as 'Lot Address',P.pincode as 'Lot Pincode',P.max_no_of_spots as 'Total Spots in Lot',P.no_of_available as 'Available Spots in Lot', P.price as 'Price per hour' FROM PARKING_LOT P WHERE {field} LIKE ? ",('%'+value+'%',))
        if field == 'spot_number':
            curr.execute(f"SELECT P.id as 'Parking Spot ID',P.spot_number as 'Spot Number',PL.prime_location as 'Lot Prime Location',PL.address as 'Lot Address',PL.pincode as 'Lot Pincode',CASE WHEN P.status='O' THEN 'Occupied' WHEN P.status = 'A' THEN 'Available' ELSE 'Unkown' END as 'Spot Status' FROM PARKING_SPOT P JOIN PARKING_LOT PL ON PL.id = P.lot_id WHERE {field} LIKE ? ",('%'+value+'%',))
        if field == 'vehicle_number':
            curr.execute(f"SELECT B.id as 'Booking ID',B.vehicle_number as 'Vehicle Number',U.email as 'User Email',U.name as 'User Name',B.spot_number as 'Sot Number',PL.prime_location as 'Lot Prime Location Name',CASE WHEN B.timestamp_booked IS NOT NULL THEN datetime(B.timestamp_booked,'unixepoch') ELSE '-' END AS 'Parking Time', CASE WHEN B.timestamp_released IS NOT NULL AND B.timestamp_released !='' THEN B.timestamp_released ELSE '-' END AS 'Release Time',CASE WHEN B.booking_status='open' THEN 'Occupied' WHEN B.booking_status = 'closed' THEN 'Parked Out' ELSE 'Unkown' END as 'Spot Status' FROM BOOKING_DETAILS B JOIN PARKING_SPOT P ON P.spot_number = B.spot_number AND P.lot_id = B.lot_id JOIN PARKING_LOT PL ON PL.id=P.lot_id  JOIN USERS U on U.id=B.user_id WHERE {field} LIKE ? ",('%'+value+'%',))
        
        results = curr.fetchall()
        if results:
            columns = results[0].keys()
        else:
            columns = []
            flash("No results found","danger")
        conn.close()
    return render_template('admin/admin_search.html',results=results,columns=columns)

@admin_view.route('/summary')
@admin_required
def admin_summary():
    conn = conn_database()
    curr = conn.cursor()

    curr.execute("SELECT COUNT(*) FROM USERS WHERE is_admin=0")
    total_users = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM USERS WHERE is_admin=1")
    total_admins = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM PARKING_LOT")
    total_lots = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM PARKING_SPOT")
    total_spots = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM PARKING_SPOT WHERE status='A'")
    available_spots = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS")
    booked_spots = curr.fetchone()[0]

    curr.execute("SELECT COUNT(*) FROM BOOKING_DETAILS WHERE booking_status='open'")
    active_bookings = curr.fetchone()[0]

    curr.execute('''
        SELECT id, prime_location, max_no_of_spots, no_of_available, price FROM PARKING_LOT
    ''')
    lot_data = curr.fetchall()

    curr.execute('''
        SELECT U.name, B.vehicle_number, B.spot_number, B.timestamp_booked, B.booking_status, P.lot_id
        FROM BOOKING_DETAILS B
        JOIN USERS U ON B.user_id = U.id
        JOIN PARKING_SPOT P ON B.spot_number = P.spot_number AND P.lot_id = B.lot_id
        ORDER BY B.timestamp_booked DESC LIMIT 10
    ''')
    recent_bookings = curr.fetchall()

    conn.close()
    return render_template('admin/admin_summary.html',
                           total_users=total_users,
                           total_admins=total_admins,
                           total_lots=total_lots,
                           total_spots=total_spots,
                           available_spots=available_spots,
                           booked_spots=booked_spots,
                           active_bookings=active_bookings,
                           lot_data=lot_data,
                           recent_bookings=recent_bookings)

@admin_view.route('/edit_profile',methods=['POST','GET'])
@admin_required
def admin_profile():
    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM USERS WHERE id = ?',(session['id'],))
    admin = curr.fetchone()
    conn.close()

    id = admin['id']
    
    if request.method == 'POST':
        email = request.form['email']

        conn = conn_database()
        curr = conn.cursor()

        query = "UPDATE USERS SET email = ?,name =?, address = ?, pincode = ? WHERE id =?"
        data = (email,request.form['name'],request.form['address'],request.form['pincode'],id)

        curr.execute(query,data)
        conn.commit()
        conn.close()
        flash("Profile Updated","success")
        return redirect(url_for('admin.admin_profile'))
    
    return render_template('admin/admin_edit_profile.html',admin=admin)

@admin_view.route('logout')
@admin_required
def admin_logout():
    session.clear()
    flash("Logged Out Successfully","success")
    return redirect(url_for('base.user_login'))
    

