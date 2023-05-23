from flask import Flask,request,session,render_template,redirect,url_for
import mysql.connector
from datetime import date
#MySQL connection.
submitted = False
mydb = mysql.connector.connect(
    host="uzb4o9e2oe257glt.cbetxkdyhwsb.us-east-1.rds.amazonaws.com	",
    user="wtnvl78jqm6l1o3i",
    password="x0c0j8n14k1ojywa",
    database = 'e17eftfl4xnppbsr',
    auth_plugin='mysql_native_password'
    )
app = Flask(__name__)
app.secret_key = "TESTVALUE"
@app.route('/')

@app.route('/home', methods=['GET', 'POST'])
def index():
#Requires collection of all property image files.
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT picture FROM propertyforrent')
    myres = mycursor.fetchall()
    images = []
    for i in myres:
        images.append(i)
    return render_template('home.html',images=images)

@app.route('/signout')
def signout():
    session.pop('id')
    return redirect(url_for('index'))

@app.route('/Login')
def login():
    
    return render_template('login.html')

@app.route('/Login', methods=['POST'])
def login_post():
    vals = {}
    #Requires finding email and password, then creation of Session.
    vals["email"] = request.form["email"]
    vals["postcode"] = request.form["postcode"]
    if 'id' in session:
        error = f'Already logged in! {session["id"]}'
        return render_template('login.html',error=error)
    availUser = checkLogin(vals["email"], vals["postcode"])
    if availUser == -1:
        error = "No User Available.. Please try again!"
        return render_template('login.html',error=error)
    else:
        session['id'] = availUser
        session['submitted'] = False
        return redirect(url_for('index'))
#Removed 04/22/23
# @app.route('/Register')
# def register():
    
#     return render_template('register.html')

@app.route('/BookView',methods=['GET','POST'])
def bookview():
    vals = {}
    properties = []
    mycursor2 = mydb.cursor()
    mycursor2.execute("SELECT propertyNo, street FROM propertyforrent")
    props = mycursor2.fetchall()
    for i in props:
        if i[0] not in properties:
            properties.append(i[0])

    if request.method == 'POST':
    
        logged = False
        if 'id' in session:
            logged = True
            vals["propno"] = str(request.form["propno"])
            vals["date"] = str(request.form["date"])
            vals["hour"] = str(request.form["hour"] + ":00")
            mycursor = mydb.cursor()
            mycursor.execute('INSERT INTO Viewing(clientNo, propertyNo, viewDate, viewHour) VALUES (%s,%s, %s, %s)',(session['id'],vals["propno"],vals["date"],vals["hour"]))
            mydb.commit()
        else:
            logged = False
    else:
        if 'id' in session:
            logged = True
        else:
            logged = False
    return render_template('bookview.html',logged=logged,vals=vals,properties=properties)

@app.route('/Rentals', methods=['GET','POST'])
def rentals():
    vals = {}
    postlist = []
    typelist = []
    selProps = []
    val = ()
    request.close()
    sql = "SELECT p.propertyNo as ID, p.street, p.city, p.postcode, s.fName, s.lName, p.rooms, p.rent, p.propertyType FROM propertyforrent as p INNER JOIN staff as s ON s.staffNo=p.staffNo "
    sql2 = ''
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT postcode, propertyType FROM propertyforrent')
    myres = mycursor.fetchall()
    for x in myres:
        if x[0] not in postlist:
            postlist.append(x[0])
        if x[1] not in typelist:
            typelist.append(x[1])
        session['submitted'] = False
        if request.method == 'POST':
            vals["area"] = request.form["area"]
            vals["type"] = request.form["type"]
            vals["size"] = request.form["size"]
            vals["maxRent"] = request.form["maxRent"]
            if vals["area"] == "any" and vals["type"] == "any":
                sql2 = sql + "WHERE p.rooms >= %s AND p.rent <= %s"
                val = (vals["size"],vals["maxRent"])
                # mycursor.execute(sql,val)
            elif vals["area"] == "any":
                sql2 = sql + "WHERE p.propertyType = %s AND p.rooms >= %s AND p.rent <= %s"
                val = (vals["type"], vals["size"],vals["maxRent"])
                # mycursor.execute(sql,val)
            elif vals["type"] == "any":
                sql2 = sql + "WHERE p.postcode = %s AND p.rooms >= %s AND p.rent <= %s"
                val = (vals["area"], vals["size"],vals["maxRent"])
                # mycursor.execute(sql,val)
            else:
                sq2 = sql + "WHERE p.postcode = %s AND p.propertyType = %s AND p.rooms >= %s AND p.rent <= %s"
                val = (vals["area"],vals["type"], vals["size"],vals["maxRent"]) 
            sql2 = sql2 + "ORDER BY p.rooms"
            mycursor.execute(sql2,val)
            curProps = mycursor.fetchall()
            for i in curProps:
                if i not in selProps:
                    selProps.append(i)

    return render_template('Rentals.html',properties=postlist,types=typelist,selProps=selProps)

@app.route('/AddtoMail', methods=['GET'])
def addtomail():
    #Handles only the initial loading.
    return render_template('addtomail.html')

@app.route('/AddtoMail', methods=['POST'])
def addtomail_post():
    conf = ''
    error = ''
    vals = {}
    #Requires to check if an account already exists. if not, add a line item.
    if request.method == 'POST':
        entered = True
        vals["fName"] = request.form['fname']
        vals["lName"] = request.form['lname']
        vals["telNo"] = request.form['telNo']
        vals["addr"] = request.form['street']
        vals["city"] = request.form['city']
        vals["postcode"] = request.form['PostCode']
        vals["email"] = request.form['email']
        vals["region"] = request.form['region']
        vals["rentPref"] = request.form['prefType']
        vals["maxRent"] = request.form['maxRent']
        alreadyJoined = checkLogin(vals["email"], vals["postcode"])
        if alreadyJoined != -1:
            conf = "Already Joined!"
        else:
            conf = "Creating account.."
            for k,v in vals.items():
                if v == '':
                    vals[k] = None
            cursor = mydb.cursor()
            cursor.execute("INSERT INTO Client (fName,lName,telNo,street,city,postCode,email,Region,preType,maxRent,joinedOn) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)",(vals["fName"],vals["lName"],vals["telNo"],vals["addr"],vals["city"],vals["postcode"],vals["email"],vals["region"],vals["rentPref"],vals["maxRent"],date.today()))
            mydb.commit()
            return redirect(url_for('login'))
    return render_template('addtomail.html',message=conf)

# @app.route('/Property')
# def property():
#     return render_template('property.html')
#Removed 04/22/23 -- Unused.


def checkLogin(email, postcode):
    mycursor = mydb.cursor()
    mycursor.execute(f'SELECT ID, email, postCode FROM Client WHERE email = "{email}" AND postCode = "{postcode}"')
    myres = mycursor.fetchall()
    if not myres:
        return -1
    else:
        return myres[0][0]

if __name__ == '__main__':
    app.run(port=8080,debug=False)
    