#!flask/bin/python
from __future__ import print_function
from flask import Flask, jsonify, abort, request, make_response, url_for
from flask import render_template, redirect
import sys
import pymysql.cursors
from credentials import temp_login
from random import randint
import hashlib

app = Flask(__name__, static_url_path="")

profile_pages = {"ADMIN":"admin.html","VISITOR":"visitor.html","OWNER":"owner.html"}
user_name = ""
def random_with_N_digits(n):
    range_start = 10**(n-1)
    range_end = (10**n)-1
    return randint(range_start, range_end)

def yesno_to_bool(str):
    if(str.lower() == "yes"):
        return 1
    else:
        return 0

def connectDB():
    connection = pymysql.connect(host= temp_login['SERVER_ADDRESS'],
                                 user= temp_login['USERNAME'],
                                 password= temp_login['PASSWORD'],
                                 db= temp_login['DB'],
                                 charset='utf8mb4',
                                 cursorclass=pymysql.cursors.DictCursor)
    return connection

@app.route('/', methods=['GET'])
def home():
    #return render_template('login_new.html')
    return render_template('login_new.html')

@app.route('/login', methods=['POST'])
def login():
    msg = request.form
    h= hashlib.md5()
    sql = "SELECT * from User WHERE Username = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql, (msg['username'],))
        results = cur.fetchone()

    conn.close()
    if(results is not None):
        h.update(msg['password'])
        if(str(results['Password']) ==  str(h.hexdigest())):
            ##change to profile pages once done
            user_type = results['UserType']
            resp = make_response(redirect("/"+ user_type))
            resp.set_cookie('type', user_type)
            resp.set_cookie('username', msg['username'])
            global user_name
            user_name = msg['username']
            return resp
    else:
        return redirect("/")

@app.route('/VISITOR', methods=['GET'])
def visitor_profile():
   name = request.cookies.get('username')
   conn = connectDB()
   sql = "SELECT Property.ID, Property.Name, Property.Street, Property.IsCommercial, Property.IsPublic, Property.City, Property.Zip, Property.PropertyType, Property.ApprovedBy, Property.Size,  Avg(Visit.Rating) as Rating, count(Visit.PropertyID) as Visits from Property JOIN Visit ON Property.ID = Visit.PropertyID AND Property.ApprovedBy != 'NULL' Group By Property.ID"
   with conn.cursor() as cur:
       cur.execute(sql)
       results = cur.fetchall()
   conn.close()
   if(request.cookies.get('type') == 'VISITOR'):
       return render_template("all_public_validated_properties.html", plist=results)
   else:
       return redirect('/')

@app.route('/OWNER', methods=['GET'])
def owner_profile():
    name = request.cookies.get('username')
    conn = connectDB()
    sql = "SELECT *,count(ID) as Visits, avg(Rating) as AvgRating from Property JOIN Visit ON Property.ID = Visit.PropertyID AND Property.Owner = %s Group By ID"
    with conn.cursor() as cur:
        cur.execute(sql, (name,))
        results = cur.fetchall()
    conn.close()
    if(request.cookies.get('type') == 'OWNER'):
        return render_template("admin_property_management.html", plist=results)
    else:
        return redirect('/')

@app.route('/ADMIN', methods=['GET'])
def admin_profile():
    if(request.cookies.get('type') == 'ADMIN'):
        return render_template("admin_functionality.html")
    else:
        if(request.cookies.get('type') == 'OWNER'):
            return redirect('/OWNER')
        else:
            return redirect('/VISITOR')

@app.route('/ownerRegisterPage', methods=['POST'])
def owner_register_page():
    return render_template("new_owner_registration.html")

@app.route('/visitorRegisterPage', methods=['POST'])
def visitor_register_page():
    return render_template("new_visitor_registration.html")

@app.route('/logout', methods=['POST'])
def logout_user():
    print("working")
    resp = make_response(redirect("/"))
    resp.set_cookie('type', expires=0)
    return resp

@app.route('/registerOwner', methods=['POST'])
def register_owner():
    conn = connectDB()
    h = hashlib.md5()
    msg = request.form
    pw = msg['password']
    h.update(pw)
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO User (Username, Email, Password, UserType) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (msg['username'],msg['email'],h.hexdigest(),'Owner'))

        conn.commit()
        isPublic = yesno_to_bool(msg['public'])
        isCommercial = yesno_to_bool(msg['isCommercial'])
        with conn.cursor() as cur:
            sql = "INSERT INTO Property (ID, Name, Size, Street, City, Zip, IsPublic, IsCommercial, PropertyType, Owner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
            cur.execute(sql, (random_with_N_digits(5), msg['propertyName'], int(msg['acres']),msg['streetAddress'],msg['city'], msg['zip'], isPublic, isCommercial, msg['propertyType'], msg['username']))

        conn.commit()
    except Exception as e:
        print(e)
    finally:
        conn.close()
        return redirect("/")

@app.route('/registerVisitor', methods=['POST'])
def register_visitor():
    h = hashlib.md5()
    conn = connectDB()
    msg = request.form
    pw = msg['password']
    h.update(pw)
    password = str(h.hexdigest())
    try:
        with conn.cursor() as cur:
            sql = "INSERT INTO User (Username, Email, Password, UserType) VALUES (%s, %s, %s, %s)"
            cur.execute(sql, (msg['username'],msg['email'],password,'Visitor'))

        conn.commit()

    except Exception as e:
        print(e)
    finally:
        conn.close()
        return redirect("/")

@app.route('/manageProperty', methods=['GET'])
def manage_property():
    pid = request.cookies.get('PropertyID')
    sql = "SELECT * from Property WHERE ID = %s"
    sql2 = "SELECT * from FarmItem WHERE IsApproved = 1 AND Type = 'ANIMAL'"
    sql3 = "SELECT * from FarmItem WHERE IsApproved = 1 AND Type != 'ANIMAL'"
    sql4 = "SELECT * from Has JOIN FarmItem On FarmItem.Name=Has.ItemName AND PropertyID=%s AND Type='ANIMAL'"
    sql5 = "SELECT * from Has JOIN FarmItem On FarmItem.Name=Has.ItemName AND PropertyID=%s AND Type!='ANIMAL'"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql, (pid,))
        result = cur.fetchone()

    with conn.cursor() as cur:
        cur.execute(sql2)
        animals_approved = cur.fetchall()

    with conn.cursor() as cur:
        cur.execute(sql3)
        crops_approved = cur.fetchall()

    with conn.cursor() as cur:
        cur.execute(sql4, (pid,))
        animals = cur.fetchall()

    with conn.cursor() as cur:
        cur.execute(sql5, (pid,))
        crops = cur.fetchall()

    conn.close()
    return render_template("manage_farm_name.html", result=result, animals=animals, crops=crops, crops_approved = crops_approved, animals_approved=animals_approved)

@app.route('/confirmedProperties', methods=['POST'])
def confirmed_properties():
    sql = "SELECT Property.ID, Property.Name, Property.Street, Property.IsCommercial, Property.IsPublic, Property.City, Property.Zip, Property.PropertyType, Property.ApprovedBy, Property.Size,  Avg(Visit.Rating) as Rating from Property JOIN Visit ON Property.ID = Visit.PropertyID AND Property.ApprovedBy != 'NULL' Group By Property.ID"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        plist = cur.fetchall()

    conn.close()
    return render_template("confirmed_properties.html", plist=plist)

@app.route('/visit_history', methods=['GET'])
def visit_history():
   sql = "SELECT Name, VisitDate, Rating, Property.ID  from Visit Join Property on Visit.PropertyID = Property.ID WHERE Username = %s"
   conn = connectDB()

   with conn.cursor() as cur:
       cur.execute(sql,(user_name))
       plist = cur.fetchall()
   print(plist)
   conn.close()
   return render_template("visit_history.html", plist=plist)

@app.route('/addPropertyView', methods=['GET'])
def add_p_view():
    sql = "SELECT * from FarmItem WHERE IsApproved = 1 AND Type = 'ANIMAL'"
    sql2 = "SELECT * from FarmItem WHERE IsApproved = 1 AND Type != 'ANIMAL'"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        animals = cur.fetchall()

    with conn.cursor() as cur:
        cur.execute(sql2)
        crops = cur.fetchall()

    conn.close()
    return render_template("add_new_property.html", animals=animals, crops=crops)

@app.route('/addProperty', methods=['POST'])
def add_property():
    msg = request.form
    sql = "INSERT INTO Property (ID, Name, Size, Street, City, Zip, IsPublic, IsCommercial, PropertyType, Owner) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)"
    conn = connectDB()
    isPublic = yesno_to_bool(msg['public'])
    isCommercial = yesno_to_bool(msg['commercial'])
    global user_name
    with conn.cursor() as cur:
        cur.execute(sql, (random_with_N_digits(5), msg['name'], int(msg['size']),msg['street'],msg['city'], msg['zip'], isPublic, isCommercial, msg['propertyType'], user_name))
    conn.commit()
    with conn.cursor() as cur:
        cur.execute(sql, (random_with_N_digits(5), msg['name'], int(msg['size']),msg['street'],msg['city'], msg['zip'], isPublic, isCommercial, msg['propertyType'], user_name))
    conn.commit()
    conn.close()
    return redirect("/OWNER")

@app.route('/unconfirmedProperties', methods=['POST'])
def unconfirmed_properties():
    sql = "SELECT * from Property WHERE ApprovedBy = 'NULL'"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        plist = cur.fetchall()

    conn.close()
    return render_template("unconfirmed_properties.html", plist=plist)

@app.route('/ownerList', methods=['POST'])
def owner_list():
    sql = "SELECT User.Username, User.Email, count(Property.Owner) as Properties from User JOIN Property ON User.Username = Property.Owner Group By User.Username"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        olist = cur.fetchall()

    conn.close()
    return render_template("all_owners_in_system.html", olist=olist)

@app.route('/visitorList', methods=['POST'])
def visitor_list():
    sql = "select * from (SELECT User.Username, User.Email, User.UserType, count(Visit.Username) as Visits from User left JOIN Visit ON User.Username = Visit.Username AND User.UserType = 'VISITOR' Group By User.Username) p where p.UserType = 'VISITOR';"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        vlist = cur.fetchall()

    conn.close()
    return render_template("all_visitors_in_system.html", vlist=vlist)

@app.route('/viewOtherProperties', methods=['GET'])
def view_other_properties():
    sql = "SELECT Property.ID, Property.Name, Property.Street, Property.IsCommercial, Property.IsPublic, Property.City, Property.Zip, Property.PropertyType, Property.Size,  Avg(Visit.Rating) as Rating, Count(Visit.PropertyID) as Visits from Property JOIN Visit ON Property.ID = Visit.PropertyID AND Property.ApprovedBy != 'NULL' Group By Property.ID"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        plist = cur.fetchall()

    conn.close()
    return render_template("all_other_valid_properties.html", plist=plist)

@app.route('/deleteVacc', methods=['GET'])
def delete_vacc():
    name = request.cookies.get('VName')
    sql = "DELETE FROM User WHERE Username = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql,(name,))

    conn.close()
    return redirect("/ADMIN")

@app.route('/deleteOwner', methods=['GET'])
def delete_owner():
    name = request.cookies.get('OName')
    sql = "DELETE FROM User WHERE Username = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql,(name,))

    conn.close()
    return redirect("/ADMIN")

@app.route('/farmDetails', methods=['GET'])
def farm_details():
    pid = request.cookies.get('PID')
    sql = "SELECT * FROM User JOIN Property ON Property.Owner=User.Username AND Property.ID = %s"
    sql2 = "SELECT Count(Username) as Visits, Avg(Rating) as Rating from Visit WHERE PropertyID = %s"
    sql3 = "SELECT Has.ItemName, FarmItem.`Type` FROM FarmItem Join Has On FarmItem.Name=Has.ItemName AND Has.PropertyID = %s AND FarmItem.`Type` = 'ANIMAL'"
    sql4 = "SELECT Has.ItemName, FarmItem.`Type` FROM FarmItem Join Has On FarmItem.Name=Has.ItemName AND Has.PropertyID = %s AND FarmItem.`Type` != 'ANIMAL'"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql,(pid,))
        pdetails = cur.fetchone()

    with conn.cursor() as cur:
        cur.execute(sql2,(pid,))
        rating = cur.fetchone()

    with conn.cursor() as cur:
        cur.execute(sql3,(pid,))
        animals = cur.fetchall()

    with conn.cursor() as cur:
        cur.execute(sql4,(pid,))
        crops = cur.fetchall()
    conn.close()
    return render_template("company_details.html", pdetails=pdetails, rating=rating, animals=animals,crops=crops)

@app.route('/deleteVlog', methods=['GET'])
def delete_vlog():
    name = request.cookies.get('VName')
    sql = "DELETE FROM Visit WHERE Username = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql,(name,))

    conn.close()
    return redirect("/ADMIN")

@app.route('/approvedAC', methods=['POST'])
def approved_ac():
    sql = "SELECT * from FarmItem WHERE IsApproved = 1"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        aclist = cur.fetchall()

    conn.close()
    return render_template("approved_animals_crops.html", aclist=aclist)

@app.route('/addAC', methods=['GET'])
def add_ac():
    name = request.cookies.get('ACName')
    type = request.cookies.get('Type')
    conn = connectDB()
    sql = "INSERT INTO FarmItem (Name, IsApproved, Type) VALUES (%s, %s, %s)"

    with conn.cursor() as cur:
        cur.execute(sql, (name, 1 ,type))
    conn.commit()
    conn.close()
    return redirect("/ADMIN")

@app.route('/pendingAC', methods=['POST'])
def pending_ac():
    sql = "SELECT * from FarmItem WHERE IsApproved = 0"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql)
        aclist = cur.fetchall()

    conn.close()
    return render_template("pending_approval_animal_crops.html", aclist=aclist)

@app.route('/approveAC', methods=['GET'])
def approve_ac():
    name = request.cookies.get('ACName')
    sql = "UPDATE FarmItem SET IsApproved=1 WHERE Name = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql,(name,))
        aclist = cur.fetchall()

    conn.close()
    return redirect("/ADMIN")

@app.route('/deleteAC', methods=['GET'])
def delete_ac():
    name = request.cookies.get('ACName')
    sql = "DELETE FROM FarmItem WHERE Name = %s"
    conn = connectDB()

    with conn.cursor() as cur:
        cur.execute(sql,(name,))
        aclist = cur.fetchall()

    conn.close()
    return redirect("/ADMIN")

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
