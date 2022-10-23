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
import os
import sqlalchemy
from sqlalchemy.types import JSON
from sqlalchemy.ext.mutable import MutableDict
from sqlalchemy import select
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
CORS(app)
mail= Mail(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'sql6.freemysqlhosting.net'
app.config['MYSQL_USER'] = 'sql6528588'
app.config['MYSQL_PASSWORD'] = 'zku53UvvBh'
app.config['MYSQL_DB'] = 'sql6528588'
temp=app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://sql6528588:zku53UvvBh@sql6.freemysqlhosting.net:3306/sql6528588' 
# “dialect+driver://username:password@host:port/database”
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'eventabloom@gmail.com'
app.config['MAIL_PASSWORD'] = 'EnterEmailAPIKey'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mysql = MySQL(app)
mail= Mail(app)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False


db=SQLAlchemy(app)



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
    return " "
    
 
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
    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json and 'password' in request.json and 'email' in request.json  and 'isOwner' in request.json and 'age' in request.json and 'gender' in request.json and 'isAvailable' in request.json and 'bio' in request.json and 'categoryType' in request.json and 'categoryLevel' in request.json and 'city' in request.json and 'state' in request.json:
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
        age=request.json['age']
        gender=request.json['gender']
        isAvailable=request.json['isAvailable']
        bio=request.json['bio']
        categoryType=request.json['categoryType']
        categoryLevel=request.json['categoryLevel']
        city=request.json['city']
        state=request.json['state']
        token="N"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userName = % s', (username, ))
        account = cursor.fetchone()
        if account:
            msg = 'Account already exists !'
            return ({'status':'FAIL'}) 
        # elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
        #     msg = 'Invalid email address !'
        #     return ({'status':'FAIL'}) 
        # elif not re.match(r'[A-Za-z0-9]+', username):
        #     msg = 'Username must contain only characters and numbers !'
        #     return ({'status':'FAIL'}) 
        # elif not username or not password or not email:
        #     msg = 'Please fill out the form !'
        #     return ({'status':'FAIL'}) 
        else:
            cursor.execute('INSERT INTO accounts VALUES (%s,%s, % s, % s, % s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)', (first_name,last_name,username, password, email,owner,token,age,gender , isAvailable,bio, categoryType, categoryLevel, city, state))

            mysql.connection.commit()
            return ({'status':'OK'})
    elif request.method == 'POST':
        return ({'status':'FAIL'}) 
    return ""

@app.route('/speciallogin', methods =['GET', 'POST'])
def speciallogin():
    msg = ''

    if request.method == 'POST' and 'email' in request.json:

        
        email = request.json['email']  
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
                    'isOwner':account['isOwner'],
                    'age':account['age'],
                    'gender':account['gender'],
                    'isAvailable':account['isAvailable'],
                    'bio':account['bio'],
                    'categoryType':account['categoryType'],
                    'categoryLevel':account['categoryLevel'],
                    'city':account['city'],
                    'state':account['state']
                }})
            
        else:
            
            return jsonify({'status':'FAIL'})
    return " "

@app.route('/specialregister', methods =['GET', 'POST'])
def specialregister():
    msg = ''
    print(request.method)

    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json  and 'email' in request.json  and 'isOwner' in request.json and 'age' in request.json and 'gender' in request.json and 'isAvailable' in request.json and 'bio' in request.json and 'categoryType' in request.json and 'categoryLevel' in request.json and 'city' in request.json and 'state' in request.json:
        first_name = request.json['firstName']
        last_name = request.json['lastName']
        username = request.json['userName']
        email = request.json['email']
        age=request.json['age']
        gender=request.json['gender']
        isAvailable=request.json['isAvailable']
        bio=request.json['bio']
        categoryType=request.json['categoryType']
        categoryLevel=request.json['categoryLevel']
        city=request.json['city']
        state=request.json['state']
        owner=request.json['isOwner']
        token="N"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)   
    
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        
        cursor.execute('SELECT userName FROM accounts')
        accountList = cursor.fetchall()
        takenList = []
        for val in accountList:
            takenList.append(val['userName'])

        print(takenList)
        if username in takenList:
            return jsonify({'status':'FAIL'})

     
        cursor.execute('INSERT INTO accounts VALUES (%s,%s, % s, % s, % s,%s, %s,%s,%s,%s,%s,%s,%s,%s,%s)', (first_name,last_name,username, "null",email,owner,token,age,gender , isAvailable,bio, categoryType, categoryLevel, city, state ))
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
            'isOwner':account['isOwner'],
            'age':account['age'],
            'gender':account['gender'],
            'isAvailable':account['isAvailable'],
            'bio':account['bio'],
            'categoryType':account['categoryType'],
            'categoryLevel':account['categoryLevel'],
            'city':account['city'],
            'state':account['state']
            }})
        else:
            return jsonify({'status':'FAIL'})

    else:
        return jsonify({'status':'FAIL'})

    return ""




@app.route('/edit', methods =['GET', 'POST'])
def edit():
    msg = ''
    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json and 'password' in request.json and 'email' in request.json  and 'isOwner' in request.json and 'age' in request.json and 'gender' in request.json and 'isAvailable' in request.json and 'bio' in request.json and 'categoryType' in request.json and 'categoryLevel' in request.json and 'city' in request.json and 'state' in request.json:
        print(request.json)
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
        age=request.json['age']
        gender=request.json['gender']
        isAvailable=request.json['isAvailable']
        bio=request.json['bio']
        categoryType=request.json['categoryType']
        categoryLevel=request.json['categoryLevel']
        city=request.json['city']
        state=request.json['state']
        token="N"
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE userName = % s', (username, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('Update accounts SET firstName=%s, lastName=%s , password=%s, email=%s , isOwner=%s, age=%s, gender=%s, isAvailable=%s, bio=%s, categoryType=%s, categoryLevel=%s, city=%s, state=%s WHERE userName = %s', (first_name,last_name, password, email,owner,age,gender , isAvailable,bio, categoryType, categoryLevel, city, state, username,))
            mysql.connection.commit()
            cursor.execute('SELECT * FROM accounts WHERE userName = % s', (username, ))
            account = cursor.fetchone()
            print(account)
            return jsonify({'status': 'OK',
            'body':{
                
                'firstName':account['firstName'],
            'lastName':account['lastName'],
            'userName':account['userName'],
            'email':account['email'],
            'isOwner':account['isOwner'],
            'age':account['age'],
            'gender':account['gender'],
            'isAvailable':account['isAvailable'],
            'bio':account['bio'],
            'categoryType':account['categoryType'],
            'categoryLevel':account['categoryLevel'],
            'city':account['city'],
            'state':account['state']


            }})
        else:
            return ({'status':'FAIL'})
    
    return ""

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
    return ""

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

    return ""


@app.route('/registervenue', methods =['GET', 'POST'])

def registervenue():
    
    if request.method == 'POST' and 'venueOwner' in request.json and 'venueName' in request.json and 'venueAddress' in request.json and 'venueAvailability' in request.json  and 'venueOpen' in request.json and 'venueHrCost' in request.json and 'venueCategory' in request.json:
        with open('counter.txt','r') as f:
            venueId=f.read()
            print(venueId)
        with open('counter.txt','w') as f:
            f.write(str(int(venueId)+1))
            
        
        venueOwner = request.json['venueOwner']
        venueName = request.json['venueName']
        venueAddress= request.json['venueAddress']
        venueAvailability=request.json['venueAvailability']
        venueOpen=request.json['venueOpen']
        venueHrCost=request.json['venueHrCost']
        venueCategory=request.json['venueCategory']
        venueCity=request.json['venueCity']
        venueState=request.json['venueState']
        venueState=request.json['venueDescription']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT INTO Venue VALUES (%s,%s, % s, %s, %s, %s,%s,%s, %s,%s,%s)', (venueId,venueOwner,venueName, venueAddress, venueAvailability,venueOpen,venueHrCost,venueCategory,venueCity,venueState, venueDescription,))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM  Venue')
        data= cursor.fetchall() 
        arr=[]

        return jsonify({
        'body':list(data),
        'status':'OK'
        })
    elif request.method == 'POST':
        return jsonify({'status':'FAIL'})

    return ""

@app.route('/venuelist', methods =['GET', 'POST'])

def venuelist():

    if request.method == 'GET':
        print(request.method)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM  Venue')
        data= cursor.fetchall() 
    
        return jsonify({
        'body':list(data),
        'status':'OK'
        })
    
    return jsonify({
        'body': {},
        'status':'FAIL'
        })
    
# /EnterUserName's code for useractivitylist inserting into db and returning back from db.
        

# @app.route("/")
# def hello():
#     return "Welcome to backend"

@app.route("/activity",methods=['POST'])
def factivity():
    got=request.get_json()

    print(got)
    actobj=Activities(
        activityName=got['activityName'],
        activityDescription=got['activityDescription'],
        activityOrganizer=got['activityOrganizer'],
        activityVenueId=got['activityVenueId'],
        activityVenueName=got['activityVenueName'],
        activityVenueAddress=got['activityVenueAddress'],
        activityLocation=got['activityLocation'],
        activityDate=got['activityDate'],
        activityTime=got['activityTime'],
        activityCity=got['activityCity'],
        activityState=got['activityState'],
        activityCategory=got['activityCategory'],
        activityAgeRange=got['activityAgeRange'],
        activityCost=got['activityCost']
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
        all_activities=[{ "activityName":Activities.activityName,
        "activityDescription":Activities.activityDescription,
        "activityOrganizer":Activities.activityOrganizer,
        "activityVenueId":Activities.activityVenueId,
        "activityVenueName":Activities.activityVenueName,
        "activityVenueAddress":Activities.activityVenueAddress,
        "activityLocation":Activities.activityLocation,
        "activityDate":Activities.activityDate,
        "activityTime":Activities.activityTime,
        "activityCity":Activities.activityCity,
        "activityState":Activities.activityState,
        "activityCategory":Activities.activityCategory,
        "activityAgeRange":Activities.activityAgeRange,
        "activityCost":Activities.activityCost} for Activities in q]
        
        return jsonify({'status':'OK',
                        'body':all_activities})

    else:
        return ({'status':'FAIL'})

#api for user's list:
# @app.route("/users",methods=['POST'])
# def fusers():
#     got=request.get_json()#get users from request
#     print(got)#print users
#     usersobj=Accounts(
#         firstName=got['firstName'],
#         lastName=got['lastName'],
#         userName=got['userName'],
#         password=got['password'],
#         email=got['email'],
#         isOwner=got['isOwner'],
#         token=got['token'],
#         age=got['age'],
#         gender=got['gender'],
#         isAvailable=got['isAvailable'],
#         bio=got['bio'],
#         categoryType=got['categoryType'],
#         categoryLevel=got['categoryLevel'],
#         city=got['city'],
#         state=got['state']
#         )

#     db.session.add(usersobj)

#     db.session.commit()

#     print(usersobj)

#     # got=request.get_json()
#     # print(got)
#     # print(got['activityId'])
#     return ""

#api for getting from user's list

@app.route("/ru",methods=['GET'])
def returnusers():
    
    q=Accounts.query.all()
    
    if len(q):
        all_users=[{"userName":Accounts.userName,
                        "firstName":Accounts.firstName,
                        "lastName":Accounts.lastName,
                        "age":Accounts.age,
                        "gender":Accounts.gender,
                        "isAvailable":Accounts.isAvailable,
                        "bio":Accounts.bio,
                        "categoryType":Accounts.categoryType,
                        "categoryLevel":Accounts.categoryLevel,
                        "city":Accounts.city,
                        "state":Accounts.state,
                       } for Accounts in q]
        
        return jsonify({'status':'OK',
                        'body':all_users})

    else:
        return ({'status':'FAIL'})
    




class Activities(db.Model):
        activityName=db.Column(db.Integer,nullable=False)
        activityDescription=db.Column(db.Integer,nullable=False)
        activityOrganizer = db.Column(db.Integer,nullable=False)
        activityVenueId=db.Column(db.Integer,primary_key=True,nullable=False)
        activityVenueName= db.Column(db.String(100),nullable=False)
        activityVenueAddress=db.Column(db.String(10),nullable=False)
        activityLocation=db.Column(db.String(50),nullable=False)
        activityDate=db.Column(db.JSON)
        activityTime=db.Column(db.JSON)
        activityCity=db.Column(db.Text(25))
        activityState=db.Column(db.Text(25))
        activityCategory = db.Column(db.Text(25))
        activityAgeRange=db.Column(db.Text(25))
        activityCost=db.Column("activityCost", db.Text(25))


class Accounts(db.Model):
        firstName=db.Column(db.String(50),nullable=False)
        lastName=db.Column(db.String(50),nullable=False)
        userName= db.Column(db.String(50),primary_key=True,nullable=False)
        password=db.Column(db.String(50),nullable=False)
        email = db.Column(db.String(100),nullable=False)
        isOwner=db.Column(db.String(10),nullable=False)
        token=db.Column(db.String(50),nullable=False)
        age=db.Column(db.String(50),nullable=False)
        gender=db.Column(db.String(50),nullable=False)
        isAvailable=db.Column(db.String(50),nullable=False)
        bio=db.Column(db.String(50),nullable=False)
        categoryType = db.Column(db.String(50),nullable=False)
        categoryLevel=db.Column(db.String(50),nullable=False)
        city= db.Column(db.String(50),nullable=False)
        state=db.Column(db.String(50),nullable=False)
        









    


