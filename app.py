from email.message import Message
from flask_cors import CORS
import uuid
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
import hashlib
from flask import jsonify
# from init import mail

app = Flask(__name__)
CORS(app)
mail= Mail(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'sedb'


app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'eventabloom@gmail.com'
app.config['MAIL_PASSWORD'] = 'EnterEmailAPIKey'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

 
mysql = MySQL(app)
mail= Mail(app)
@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    print(request.json)
    if request.method == 'POST' and 'userName' in request.json and 'password' in request.json:
        username = request.json['userName']
        pas = request.json['password']
        print(pas)
        salt = "5gz"
        db_password = pas+salt
        pass1 = hashlib.md5(db_password.encode())
        password=pass1.hexdigest()
        print(password)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userName = % s AND password = % s', (username, password, ))
        account = cursor.fetchone()
        
        
        if account:
            session['loggedin'] = True
            session["userName"]=account["userName"]
            return jsonify({'status': 'OK',
            'body':{
                'firstName':account['firstName'],
            'lastName':account['lastName'],
            'userName':account['userName'],
            'email':account['email'],
            'isOwner':account['isOwner']}})
            # return render_template('index.html', msg = msg)
        else:
            return ({'status':'FAIL'})
    return 
    
 
@app.route('/logout',methods =['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('userName', None)
    return {
        'status':"OK"

    }
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json and 'password' in request.json and 'email' in request.json  and 'isOwner' in request.json:
        first_name = request.json['firstName']
        last_name = request.json['lastName']
        username = request.json['userName']
        pas = request.json['password']
        salt = "5gz"
        db_password = pas+salt
        pass1 = hashlib.md5(db_password.encode())
        password=pass1.hexdigest()
        email = request.json['email']
        owner=request.json['isOwner']
        token="N"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userName = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'Username must contain only characters and numbers !'
        elif not username or not password or not email:
            msg = 'Please fill out the form !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (%s,%s, % s, % s, % s,%s,%s)', (first_name,last_name,username, password, email,owner,token))
            mysql.connection.commit()
            return ({'status':'OK'})
    elif request.method == 'POST':
        return ({'status':'FAIL'}) 

@app.route('/speciallogin', methods =['GET', 'POST'])
def speciallogin():
    msg = ''

    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json  and 'email' in request.json  and 'isOwner' in request.json:

        first_name = request.json['firstName']
        last_name = request.json['lastName']
        username = request.json['userName']
        email = request.json['email']

        owner=request.json['isOwner']
        token="N"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
    
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        print(account, email)
        if account:
            return jsonify({'status': 'OK',
            'body':{
                'firstName':account['firstName'],
            'lastName':account['lastName'],
            'userName':account['userName'],
            'email':account['email'],
            'isOwner':account['isOwner']}})
            
        else:
            print("Entered User Creation")
            cursor.execute('SELECT userName FROM accounts')
            accountList = cursor.fetchall()
            takenList = []
            for val in accountList:
                takenList.append(val['userName'])
            
            if username in takenList:
                return jsonify({'status':'FAIL'})

            cursor.execute('INSERT INTO accounts VALUES (%s,%s, % s, % s, % s,%s, %s)', (first_name,last_name,username, "null",email,owner,token ))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
            account =  cursor.fetchone()

            if account:
                return jsonify({'status': 'OK',
                'body':{
                    'firstName':account['firstName'],
                'lastName':account['lastName'],
                'userName':account['userName'],
                'email':account['email'],
                'isOwner':account['isOwner']}})
            else:
                return jsonify({'status':'FAIL'})

    



@app.route('/edit', methods =['GET', 'POST'])
def edit():
    msg = ''
    print(request.json)
    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json and 'password' in request.json and 'email' in request.json  and 'isOwner' in request.json:
        first_name = request.json['firstName']
        last_name = request.json['lastName']
        username = request.json['userName']
        pas = request.json['password']
        salt = "5gz"
        db_password = pas+salt
        pass1 = hashlib.md5(db_password.encode())
        password=pass1.hexdigest()
        email = request.json['email']
        owner=request.json['isOwner']
        token="N"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userName = % s', (username, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('Update accounts SET firstName= %s, lastName= %s , password=%s, email=%s , isOwner=%s WHERE userName = % s',(first_name,last_name, password, email,owner, username))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM accounts WHERE userName = % s', (username, ))
            account = cursor.fetchone()
            return jsonify({'status': 'OK',
            'body':{
                'firstName':account['firstName'],
            'lastName':account['lastName'],
            'userName':account['userName'],
            'email':account['email'],
            'isOwner':account['isOwner']}})
        else:
            return ({'status':'FAIL'})
    

@app.route('/reset_mail', methods =['GET', 'POST'])
def reset():
    if request.method == 'POST' and 'email' in request.json:
        email = request.json['email']
        token=str(uuid.uuid4())
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg=Message("Password Reset Email", sender="eventabloom@gmail.com",recipients=[email])
            msg.body=render_template("email.txt",token=token)
            mail.send(msg)
            cursor.execute('Update accounts SET token= %s WHERE email = % s', (token,email,))
            mysql.connection.commit()
            return jsonify({"status":"OK"})
        else:
            return jsonify({"status":"FAIL"})

@app.route('/password_reset', methods =['GET', 'POST'])
def pass_reset():
    if request.method == 'POST' and 'password' in request.json:
        pas = request.json['password']
        salt = "5gz"
        db_password = pas+salt
        pass1 = hashlib.md5(db_password.encode())
        password=pass1.hexdigest()
        token = request.json['token']
        token1=str(uuid.uuid4())
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE token = % s', (token, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('Update accounts SET token= %s, password= %s WHERE token = % s', (token1,password,token,))
            mysql.connection.commit()
            return {"status": "OK"}
        else:
            return {"status":"FAIL"}
    
# /EnterUserName's code for useractivitylist inserting into db and returning back from db.
import os
import sqlalchemy
from sqlalchemy.types import JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import select
from flask import Flask
from flask import request
from flask_sqlalchemy import SQLAlchemy
from flask import jsonify

app = Flask(__name__)

temp=app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:root@localhost:3306/bloomdb' 
# os.path.join(basedir, 'database.db') 
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)

class Activities(db.Model):
        availibility=db.Column(db.JSON)
        hrcost=db.Column(db.Integer,nullable=False)
        actid = db.Column(db.Integer,primary_key=True,nullable=False)
        location=db.Column(db.String(50))
        actname = db.Column(db.String(100),nullable=False)
        actopen=db.Column(db.String(10),nullable=False)
        actowner=db.Column(db.String(50),nullable=False)
        actdesc=db.Column(db.String(50),nullable=False)
        acttype=db.Column(db.Text(25))
        actcity=db.Column(db.Text(25))
        actstate=db.Column(db.Text(25))
        actagerange = db.Column(db.Text(25))
        actcost=db.Column(db.Text(25))
        

# @app.route("/")
# def hello():
#     return "Welcome to backend"

@app.route("/activity",methods=['POST'])
def factivity():
    got=request.get_json()

    print(got)
    actobj=Activities(
        availibility=got['availibility'],
        hrcost=got['hrcost'],
        actid=got['id'],
        location=got['location'],
        actname=got['name'],
        actopen=got['isopen'],
        actowner=got['owner'],
        actdesc=got['description'],
        acttype=got['category'],
        actcity=['city'],
        actstate=got['state'],
        actagerange=got['agerange'],
        actcost=got['cost']
        )

    db.session.add(actobj)

    db.session.commit()

    print(actobj)

    # got=request.get_json()
    # print(got)
    # print(got['activityId'])
    return ""

@app.route("/ra",methods=['GET'])
def returnacts():
    
    q=Activities.query.all()
    
    if len(q):
        all_activities=[{"activityAvailibility":Activities.availibility,
                        "activityHrCost":Activities.hrcost,
                        "activityId":Activities.actid,
                        "activityLocation":Activities.location,
                        "activityName":Activities.actname,
                        "activityOpen":Activities.actopen,
                        "activityOwner":Activities.actowner,
                        "activityDescription":Activities.location,
                        "activityType":Activities.acttype,
                        "activityCity":Activities.actcity,
                        "activityState":Activities.actstate,
                        "activityAgeRange":Activities.actagerange,
                        "activityCost":Activities.actcost} for Activities in q]
        
        print(all_activities)
        return jsonify({'status':'OK',
                        'body':all_activities})

    else:
        return ({'status':'FAIL'})


    
    


