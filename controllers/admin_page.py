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
        request_name = request.form['form_type']
        if request_name == "create_lot" :
            prime_location = request.form['prime_location']
            address = request.form['address']
            pincode = request.form['pincode']
            price = request.form['price']
            max_no_of_spots = request.form['max_no_of_spots']

            conn = conn_database()
            curr = conn.cursor()

            curr.execute('INSERT INTO PARKING_LOT (prime_location,price ,address,pincode,max_no_of_spots,no_of_available) VALUES (?,?,?,?,?,?)',(prime_location,price,address,pincode,max_no_of_spots,max_no_of_spots))
            id = curr.lastrowid
            for i in range(1,int(max_no_of_spots)+1):
                spot_name = f"{prime_location} Spot # {i}"
                curr.execute('INSERT INTO PARKING_SPOT (lot_id,spot_number,status) VALUES (?,?,?)',(id,spot_name,"A"))
            conn.commit()
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
            if no_occupied == 0 and max_no_of_spots ==0:
                curr.execute('DELETE FROM PARKING_LOT WHERE id =?',(lot_id,))
     #       if max_no_of_spots< no_occupied:
     #           flash("New max spots cannot be less than currently occupied spots.", "error")
        #        conn.close()
     #           return redirect(url_for('admin.admin_home'))
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
            elif max_no_of_spots>=previous_total_spots:
                for i in range(max_no_of_spots-previous_total_spots):
                    j = previous_total_spots
                    spot_name = f"{prime_location} Spot # {j}"
                    curr.execute('INSERT INTO PARKING_SPOT (lot_id,spot_number,status) VALUES (?,?,?)',(lot_id,spot_name,'A'))
            conn.commit()
            
            conn.close()
            return(redirect(url_for('admin.admin_home')))
       
    





    conn = conn_database()
    curr = conn.cursor()
    curr.execute('SELECT * FROM PARKING_LOT')
    lots = curr.fetchall()
    spots = []
    for lot in lots:
        curr.execute('SELECT * FROM PARKING_SPOT WHERE lot_id =?',(lot['id'],))
        spots.append(curr.fetchall())
        

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
    

