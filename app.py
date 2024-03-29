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
from sqlalchemy import select,delete,update
from sqlalchemy import create_engine
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Column, ForeignKey, Integer, Table
from sqlalchemy.orm import relationship
import json
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Index, LargeBinary,BigInteger, String, Float, Text, Boolean
from sqlalchemy import create_engine
from sqlalchemy.engine.url import URL
import stripe


import os
from flask import Flask, flash, request, redirect, url_for
from werkzeug.utils import secure_filename
import base64

import pyotp
import qrcode
from IPython.display import display
from io import BytesIO
import os
from flask import send_file
import random
import string

Base = declarative_base()

app = Flask(__name__)
CORS(app)
mail= Mail(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = 'EnterDetailsHere'
app.config['MYSQL_USER'] = 'EnterUserName'
app.config['MYSQL_PASSWORD'] = '#Password'
app.config['MYSQL_DB'] = 'bloomdb'
db_uri=app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://EnterUserName:#Password@EnterDetailsHere:3306/bloomdb' 
# “dialect+driver://username:password@host:port/database”
app.config['SQLALCHEMY_TR\\ACK_MODIFICATIONS'] = False

# app.secret_key = 'your secret key'
# app.config['MYSQL_HOST'] = 'localhost'
# app.config['MYSQL_USER'] = 'root'
# app.config['MYSQL_PASSWORD'] = 'root'
# app.config['MYSQL_DB'] = 'bloomdb'
# temp=app.config['SQLALCHEMY_DATABASE_URI'] ='mysql://root:root@localhost:3306/bloomdb' 
# # “dialect+driver://username:password@host:port/database”
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
app.secret_key = 'super secret key'



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
                'userName':account['userName'],
                'firstName':account['firstName'],
                'lastName':account['lastName'],
                'age':account['age'],
                'gender':account['gender'],
                'isAvailable':account['isAvailable'],
                'bio':account['bio'],
                'categoryType':account['categoryType'],
                'categoryLevel':account['categoryLevel'],
                'city':account['city'],
                'state':account['state'],
                'email':account['email'],
                'isOwner':account['isOwner']
            }})
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
   
    if request.method == 'POST' :
        print(request.json)
        with open('venue_counter.txt','r') as f:
            venueId=f.read()
            print(venueId)
        with open('venue_counter.txt','w') as f:
            f.write(str(int(venueId)+1))
           
        venueDescription=request.json['venueDescription']
        venueAddress=request.json['venueAddress']
        venueOwner = request.json['venueOwner']
        venueName = request.json['venueName']
        venueAvailability=request.json['venueAvailability']
        venueOpen=request.json['venueOpen']
        venueHrCost=request.json['venueHrCost']
        venueCategory=request.json['venueCategory']
        venueCity=request.json['venueCity']
        venueState=request.json['venueState']

        venuedate=request.json['creationDate']
        venueslot=json.dumps(request.json['venueSlots'])
        
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

        cursor.execute('Insert into booking Values(%s,%s,%s)', (venueId,venuedate,venueslot))
        mysql.connection.commit()

        cursor.execute('INSERT INTO venue VALUES (%s,%s,%s, % s, %s, % s,%s,%s, %s,%s,%s)', (venueId,venueDescription,venueAddress,venueOwner,venueName,venueAvailability,venueOpen,venueHrCost,venueCategory,venueCity,venueState))
        mysql.connection.commit()
        cursor.execute('SELECT * FROM  Venue')
        data= cursor.fetchall()
        arr=[]

        imageobj=venueimages(venueId=venueId, venueImage=request.json['venueImage'].encode('utf-8'))
        db.session.add(imageobj)
        db.session.commit()

        return jsonify({
        'status':'OK'
        })
    elif request.method == 'POST':
        return jsonify({'status':'FAIL'})

    return ""

@app.route('/venuelist', methods =['GET', 'POST'])
def venuelist():
    if request.method == 'GET':
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
       
        cursor.execute("select venue.venueId,venueDescription,venueAddress, venueOwner,venueName,venueAvailability,venueOpen,venueHrCost,venueCategory,venueCity,venueState, CONCAT('{',GROUP_CONCAT(CONCAT(venuedate,':',venueslots)),'}') as venueSlots from venue inner join booking on venue.venueId=booking.venueId GROUP By venueId")
        data= cursor.fetchall()
        data_l=list(data)
        for i in data_l:
            i['venueSlots']=i['venueSlots'].replace('{2','{"2').replace(":",'":').replace(",2",',"2')
            a=json.loads(i['venueSlots'])
            i['venueSlots']=a
            cursor.execute("select venueimage from venueimages where venueid={}".format(i["venueId"]))
            data= cursor.fetchone()
            i['venueImage'] = str(data["venueimage"].decode("utf-8"))

            # file1 = open("MyFile.txt", "w")
            # file1.write(str())
            # file1.close()
        return jsonify({
        'body':list(data_l),
        'status':'OK'
        })

        return jsonify({
            'body': {},
            'status':'FAIL'
            })
        
   
    return jsonify({
        'body': {},
        'status':'FAIL'
        })


@app.route('/venuebooking', methods =['GET', 'POST'])
def venuebooking():

    if request.method == 'POST':

        with open('activity_counter.txt','r') as f:

            activityId=f.read()

        with open('activity_counter.txt','w') as f:

            f.write(str(int(activityId)+1))

        venueSlots=request.json['venueSlots']
        activityName=request.json['activityName']
        activityDescription=request.json['activityDescription']
        activityCapacity=request.json['activityCapacity']
        activityLocation=request.json['activityLocation']
        activityCategory=request.json['activityCategory']
        activityAgeRange=request.json['activityAgeRange']
        activityCost=request.json['activityCost']
        activityCostAmount=request.json['activityCostAmount']
        activityOrganizer=request.json['activityOrganizer']
        activityVenueId=request.json['activityVenueId']
        activityDate=request.json['activityDate']
        activityVenueCost=request.json['activityVenueCost']
        activityBookingDate=request.json['activityBookingDate']
        activityTime=request.json['activityTime']
        activityRemainingCapacity=request.json['activityRemainingCapacity']      
        venueId=request.json['activityVenueId']
        activityImage=request.json['activityImage']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('INSERT into activities Values(%s,%s,%s,%s,%s,%s,%s,%s,%s, %s, %s, % s,%s,%s, %s,%s)',(activityId,activityName,activityDescription,activityCapacity,activityLocation,activityCategory,activityRemainingCapacity,activityAgeRange,activityCost,activityCostAmount,activityOrganizer,activityVenueId,activityDate,activityTime,activityVenueCost,activityBookingDate))        
        mysql.connection.commit()
        
        imageobj=storeimages(activityId=activityId,
                                    activityImage=request.json['activityImage'].encode('utf-8'))
        db.session.add(imageobj)
        db.session.commit()
        print(imageobj)
        print("activity_information_and_image_stored_succesfullly")
        
        for i in venueSlots:
            cursor.execute('select venuedate from booking where venuedate=%s',(i,))
            isthere=cursor.fetchone()
            if isthere:
                venueslot=json.dumps(venueSlots[i])
                print(venueslot)
                cursor.execute('update booking set venueslots=%s where venuedate=%s',(venueslot,i))
                mysql.connection.commit()

                

            else:
                venueslot=json.dumps(venueSlots[i])
                cursor.execute('Insert into booking Values(%s,%s,%s)', (venueId,i,venueslot))
                mysql.connection.commit()

        cursor.execute('SELECT * FROM activities WHERE activityOrganizer = %s', (activityOrganizer, ))
        username = cursor.fetchone()
        cursor.execute('SELECT * FROM booking WHERE venueId= %s', (venueId,))
        venueid=cursor.fetchone()
        if username and venueid:
            cursor.execute('select * from accounts inner join activities  on accounts.userName=activities.activityOrganizer where activities.activityOrganizer=% s',(activityOrganizer,))
            userdata=cursor.fetchone()
            cursor.execute('select * from venue inner join booking on venue.venueId=booking.venueId where booking.venueId=% s',(venueId,))
            data=cursor.fetchone()
            
            v_name=data['venueOwner']
            cursor.execute('select email from accounts inner join venue on accounts.userName=venue.venueOwner where venue.venueOwner=%s',(v_name,))
            venue_email_dict=cursor.fetchone()

            v_email=venue_email_dict['email']
            firstName=userdata['firstName']
            lastName=userdata['lastName']
            email=userdata['email']
            venueName=data['venueName']
            venueLocation=data['venueAddress']
            venueCity=data['venueCity']
            venueState=data['venueState']
            msg=Message("Booking Confirmation", sender="eventabloom@gmail.com",recipients=[email])
            msg.body=render_template("booking.txt",venueName=venueName,venueLocation=venueLocation,venueCity=venueCity,venueState=venueState)
            mail.send(msg)
            msg=Message("Venue Booked Confirmation", sender="eventabloom@gmail.com",recipients=[v_email])
            msg.body=render_template("venue_booked.txt",firstName=firstName,lastName=lastName,email=email)
            mail.send(msg)

            return jsonify({"status": "OK"})
    else:
        return jsonify({"status":"FAIL"})

@app.route("/activity",methods=['POST'])
def factivity():
    got=request.get_json()
    actobj=Activities(
        activityId = got['activityId'],
        activityName=got['activityName'],
        activityDescription=got['activityDescription'],
        activityCapacity=got['activityCapacity'],
        activityRemainingCapacity=got['activityRemainingCapacity'],
        activityLocation=got['activityLocation'],
        activityCategory = got['activityCategory'],
        activityAgeRange=got['activityAgeRange'],
        activityCost=got['activityCost'],
        activityCostAmount=got['activityCostAmount'],
        activityOrganizer = got['activityOrganizer'],
        activityVenueId=got['activityVenueId'],
        activityDate=got['activityDate'],
        activityTime=got['activityTime'],
        activityVenueCost=got['activityVenueCost'],
        activityBookingDate=got['activityBookingDate'],
        # activityImage=got['activityImage']
        )

    imageobj=storeimages(activityId=got['activityId'],
                        activityImage=got['activityImage'].encode('utf-8'))
    db.session.add(imageobj)
    db.session.commit()

    print(imageobj)

    print("activity_information_and_image_stored_succesfullly")

    return jsonify({'status':'OK'})
    

@app.route("/ra",methods=['GET'])
def returnacts():
 
    # q=Activities.query.all()
 
    q=db.session.query(Activities,venue,storeimages).filter(Activities.activityVenueId == venue.venueId,Activities.activityId==storeimages.activityId).all()

 
    if len(q):
        all_activities=[{ "activityId":Activities.activityId,
        "activityName":Activities.activityName,
        "activityDescription":Activities.activityDescription,
        "activityCapacity":Activities.activityCapacity,
        "activityRemainingCapacity":Activities.activityRemainingCapacity,
        "activityLocation":Activities.activityLocation,
        "activityCategory":Activities.activityCategory,
        "activityAgeRange":Activities.activityAgeRange,
        "activityCost":Activities.activityCost,
        "activityCostAmount":Activities.activityCostAmount,
        "activityOrganizer": Activities.activityOrganizer,
        "activityVenueId":Activities.activityVenueId,
        "activityDate":Activities.activityDate,
        "activityTime":Activities.activityTime,
        "activityVenueCost":Activities.activityVenueCost,
        "activityBookingDate":Activities.activityBookingDate,
        "venueDescription":venue.venueDescription,
        "venueAddress":venue.venueAddress,
        "venueOwner":venue.venueOwner,
        "venueName":venue.venueName,
        "venueOpen":venue.venueOpen,
        "venueHrCost":venue.venueHrCost,
        "venueCategory":venue.venueCategory,
        "venueCity":venue.venueCity,
        "venueState":venue.venueState,
        "activityImage":storeimages.activityImage.decode('utf-8')
        } for (Activities,venue,storeimages) in q]

        print(all_activities)
 
        return jsonify({'status':'OK',
            'body':all_activities})
 
    else:
        return ({'status':'FAIL'})


# @app.route("/ra",methods=['GET'])
# def returnacts():
 
#     # q=Activities.query.all()

#     q=db.session.query(Activities, venue).filter(Activities.activityId == venue.venueId).all()

#     print(q)

#     if len(q):
#         all_activities=[{ "activityId":Activities.activityId,
#             "activityName":Activities.activityName,
#             "activityDescription":Activities.activityDescription,
#             "activityCapacity":Activities.activityCapacity,
#             "activityRemainingCapacity":Activities.activityRemainingCapacity,
#             "activityLocation":Activities.activityLocation,
#             "activityCategory":Activities.activityCategory,
#             "activityAgeRange":Activities.activityAgeRange,
#             "activityCost":Activities.activityCost,
#             "activityCostAmount":Activities.activityCostAmount,
#             "activityOrganizer": Activities.activityOrganizer,
#             "activityVenueId":Activities.activityVenueId,
#             "activityDate":Activities.activityDate,
#             "activityTime":Activities.activityTime,
#             "activityVenueCost":Activities.activityVenueCost,
#             "activityBookingDate":Activities.activityBookingDate,
#             "venueDescription":venue.venueDescription,
#             "venueAddress":venue.venueAddress,
#             "venueOwner":venue.venueOwner,
#             "venueName":venue.venueName,
#             "venueOpen":venue.venueOpen,
#             "venueHrCost":venue.venueHrCost,
#             "venueCategory":venue.venueCategory,
#             "venueCity":venue.venueCity,
#             "venueState":venue.venueState
#         } for (Activities,venue) in q]

#     return jsonify({'status':'OK',
#         'body':all_activities})

#     else:
#         return ({'status':'FAIL'})

# api for user's list:
@app.route("/users",methods=['POST'])
def fusers():
    got=request.get_json()#get users from request
    print(got)#print users
    usersobj=Accounts(
        firstName=got['firstName'],
        lastName=got['lastName'],
        userName=got['userName'],
        password=got['password'],
        email=got['email'],
        isOwner=got['isOwner'],
        token=got['token'],
        age=got['age'],
        gender=got['gender'],
        isAvailable=got['isAvailable'],
        bio=got['bio'],
        categoryType=got['categoryType'],
        categoryLevel=got['categoryLevel'],
        city=got['city'],
        state=got['state']
        )

    db.session.add(usersobj)

    db.session.commit()

    print(usersobj)

    # got=request.get_json()
    # print(got)
    # print(got['activityId'])
    return ""

# api for getting from user's list

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
                        "email":Accounts.state,
                       } for Accounts in q]
        
        return jsonify({'status':'OK',
                        'body':all_users})

    else:
        return ({'status':'FAIL'})

#Route for activity Registration.
@app.route("/RegActivity",methods=['POST'])
def reg_for_act():
    
    got=request.get_json()
    print(got)
    regactobj=regact(
        activityId = got['activityId'],
        userName=got['userName']
        )
    
    #query regact to check if entry already there.
    queryregact = db.session.query(regact).all()
    print(queryregact)

    for tuple in queryregact:
        print("failed", got['userName'], tuple)
        if (tuple.activityId==got['activityId'] and tuple.userName==got['userName']):
            print("participant has already registered")
            return jsonify({'status':'FAIL'})
    
    db.session.add(regactobj)
    db.session.commit()
    print(regactobj)



    #Decrementing activity capacity.
    regactobj.activity.activityRemainingCapacity -=1
    db.session.commit()

    activityjoin=db.session.query(Activities).filter(Activities.activityId==got['activityId']).first()
    organizer=activityjoin.activityOrganizer
    accountsjoin=db.session.query(Accounts).filter(Accounts.userName==organizer).first()
    print(Accounts.userName)
    print(organizer)
    organizeremail=accountsjoin.email
    print(organizeremail)

    useremail=db.session.query(Accounts).filter(Accounts.userName==got['userName']).first().email
    print(useremail)

    msg=Message("activity registration complete", sender="eventabloom@gmail.com",recipients=[useremail,organizeremail])
    msg.body="activity registration complete"
    mail.send(msg)

    # got=request.get_json()
    # print(got)
    # print(got['activityId'])
    return jsonify({'status':'OK'})

@app.route("/CancelActivity",methods=['POST'])
def cancel_act():
 
 got=request.get_json()
 print(got)
 
 # db.session.query(Activities).filter(Activities.activityId==
 # got['activityId']).update({Activities.activityRemainingCapacity:Activities.activityRemainingCapacity+1})
 # db.session.commit()
 activity=db.session.query(Activities).filter(Activities.activityId==got["activityId"]).first()
 activity.activityRemainingCapacity += 1
 organizer=activity.activityOrganizer
 accountsjoin=db.session.query(Accounts).filter(Accounts.userName==organizer).first()
 organizeremail=accountsjoin.email
 print(organizeremail)
 
 useremail=db.session.query(Accounts).filter(Accounts.userName==got['userName']).first().email
 print(useremail)
 venuejoin=db.session.query(venue).filter(activity.activityVenueId==venue.venueId).first()
 print(venuejoin)
 db.session.commit()
 d = db.session.query(regact).filter(regact.userName==got['userName'],
 regact.activityId==got['activityId']).all()
 print(d)
 
 for record in d:
    print(record)
 db.session.delete(record)
 db.session.commit()
 msg=Message("activity Cancellation complete", sender="eventabloom@gmail.com",recipients=[useremail])
 time=[
 "1 A.M.",
 "2 A.M.",
 "3 A.M.",
 "4 A.M.",
 "5 A.M.",
 "6 A.M.",
 "7 A.M.",
 "8 A.M.",
 "9 A.M.",
 "10 A.M.",
 "11 A.M.",
 "12 P.M.",
 "1 P.M.",
 "2 P.M.",
 "3 P.M.",
 "4 P.M.",
 "5 P.M.",
 "6 P.M.",
 "7 P.M.",
 "8 P.M.",
 "9 P.M.",
 "10 P.M.",
 "11 P.M.",
 "12 P.M.",
]
 d1="ActivityName:" + activity.activityName +"\n"
 d2="ActivityDescription:" + activity.activityDescription + "\n"
 d3="ActivityLocation:" + activity.activityLocation +"\n"
 d4="ActivityCategory:" + activity.activityCategory + "\n"
 d5="ActivityCostAmount:" + str(activity.activityCostAmount) + "\n"
 d6="ActivityTime:" + time[activity.activityTime[0]] + "-" + time[activity.activityTime[-1]] +"\n"
 d6="VenueName:" + venuejoin.venueName +"\n"
 d7="VenueAddress:" + venuejoin.venueAddress +"\n"
 d8="OrganizerEmail:" + organizeremail + "\n"
 d9="ActivityBookingDate" + activity.activityBookingDate + "\n"
# d1="ActivityName:" + activityjoin.activityName +"\n"
# d2="ActivityDescription:" + activityjoin.Description + "\n"
 msg.body=d1+d2+d3+d4+d5+d6+d7+d8+d9
 mail.send(msg)
 #Mail to organizer
 msg2=Message("activity cancellation complete", sender="eventabloom@gmail.com",recipients=[organizeremail])
 d1="ActivityName:" + activity.activityName +"\n"
 d2="ActivityTime:" + time[activity.activityTime[0]] + "-" + time[activity.activityTime[-1]] +"\n"
 d3="VenueName:" + venuejoin.venueName +"\n"
 d4="VenueAddress:" + venuejoin.venueAddress +"\n"
 d5="ParticipantName:" + got['userName'] + "\n"
 d6="ParticipantEmail:" + useremail + "\n"
 d7="ActivityBookingDate" + activity.activityBookingDate + "\n"
# d1="ActivityName:" + activityjoin.activityName +"\n"
# d2="ActivityDescription:" + activityjoin.Description + "\n"
 msg2.body=d1+d2+d3+d4+d5+d6+d7
 mail.send(msg2)
 return jsonify({'status':'OK'})

@app.route("/Registered_acts",methods=['POST'])
def acts_registered():
    gotuser=request.get_json()
    print(gotuser['userName'])

    q=db.session.query(regact.activityId).filter(regact.userName==gotuser['userName']).all()
    
    ans=[]
    for i in q:
        ans.append(i[0])
    print(ans)

    # return ""  
    return jsonify({'status':'OK',
                        'body':ans})


@app.route("/insertreview",methods=['POST'])
def insert_review():
    gotreview=request.get_json()
    # print(gotreview)

    numratings_beforeinsertion=len(activityRating.query.all())
    # print(numratings_beforeinsertion)

    reviewobj=activityRating(
    activityId = gotreview['activityId'],
    userName=gotreview['userName'],
    rating=gotreview['rating'],
    review=gotreview['review']
    )

    db.session.add(reviewobj)
    db.session.commit()

    numratings_afterinsertion=len(activityRating.query.all())
    # print(numratings_afterinsertion)

    if numratings_afterinsertion-numratings_beforeinsertion==1:
    #this means record inserted successfully
        return ({'status':'OK'})
    else:
        return ({'status':'Fail'})
    
@app.route("/returnreview",methods=['POST'])
def return_review():
    got=request.get_json()
    
    r=activityRating.query.filter(activityRating.activityId==got['activityId']).all()
    
    if len(r):
        all_reviews=[{ "reviewId":activityRating.reviewId,
        "activityId":activityRating.activityId,
        "userName":activityRating.userName,
        "rating":activityRating.rating,
        "review":activityRating.review
        
        } for activityRating in r]
        print(all_reviews)
        return jsonify({'status':'OK',
            'body':all_reviews})
    
    else:
        return ({'status':'FAIL'})

@app.route("/insertreview_venue",methods=['POST'])
def insert_review_venue():
    gotreview=request.get_json()
    # print(gotreview)
    
    numratings_beforeinsertion=len(venueRating.query.all())
    

    
    
    reviewobj=venueRating(
        venueId = gotreview['venueId'],
        userName=gotreview['userName'],
        rating=gotreview['rating'],
        review=gotreview['review']
        )

    print(gotreview['venueId'],gotreview['userName'],gotreview['rating'],gotreview['review'])
    
    db.session.add(reviewobj)
    db.session.commit()
    
    numratings_afterinsertion=len(venueRating.query.all())
    print(numratings_afterinsertion)
    
    if numratings_afterinsertion-numratings_beforeinsertion==1:
    #this means record inserted successfully
        return ({'status':'OK'})
    else:
        return ({'status':'Fail'})
 
 
@app.route("/returnreview_venue",methods=['GET'])
def return_review_venue():
    gotreview=request.get_json()
    print(gotreview)
    
    r=venueRating.query.all()
    
    if len(r):
        all_reviews=[{ "reviewId":venueRating.reviewId,
        "venueId":venueRating.venueId,
        "userName":venueRating.userName,
        "rating":venueRating.rating,
        "review":venueRating.review
        
        } for venueRating in r]
        
        return jsonify({'status':'OK',
        'body':all_reviews})
    
    else:
        return ({'status':'FAIL'})


@app.route("/activityPayment",methods=['POST'])
def activityPayment():
    gotpayment=request.get_json()
    print(gotpayment)
    
    paymentobj=activityPayment(
    activityId=gotpayment['activityId'],
    participantuserName=gotpayment['participantuserName'],
    organizeruserName=gotpayment['organizeruserName'],
    amount=gotpayment['amount']
    )
    
    db.session.add(paymentobj)
    db.session.commit()
    
    return({'status':'OK'})

@app.route('/bookmark', methods =['GET', 'POST'])
def bookmark():
    if request.method=="POST":
        userName=request.json['userName']
        favVenue=request.json['favVenue']
        print(str(favVenue))
        favActivity=request.json['favActivity']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from bookmark where userName=% s', ( userName, ))
        account = cursor.fetchone()
 
        if account:
            cursor.execute("update bookmark set favVenue = %s, favActivity = %s where userName = %s",(str(favVenue),str(favActivity), userName))
            mysql.connection.commit()
        else:
            cursor.execute("insert into bookmark values(%s,%s,%s)",(userName,str(favVenue),str(favActivity)))
            mysql.connection.commit()
        return ({'status':'OK'}) 
    else:
        return ({'status':'FAIL'})
    

    return jsonify({'status':'OK',
                        'body':userdetails})
    


@app.route('/getbookmark', methods =['GET', 'POST'])
def getbookmark():
    if request.method=="POST":
        userName=request.json['userName']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from bookmark where userName=% s', ( userName, ))
        account = cursor.fetchone()
        if not account:
            return jsonify({'status': 'OK',
            'body':{
                'userName':userName,
                'favActivity':[],
                'favVenue':[]
            }})

        else:

            if ',' not in account['favActivity']:
                account['favActivity']=account['favActivity'].strip('][')
            else:
                account['favActivity']=account['favActivity'].strip('][').split(',')
            if ',' not in account['favVenue']:
                account['favVenue']=account['favVenue'].strip('][')
            else:
                account['favVenue']=account['favVenue'].strip('][').split(',')
            favVenue=[]
            favActivity=[]

            if len(account['favVenue']) > 0 and len(account['favVenue']) <= 1:
                favVenue.append(int(account['favVenue']))
            else:
                for i in account['favVenue']:
                    favVenue.append(int(i))
            
            if len(account['favActivity']) > 0 and len(account['favActivity']) <= 1:
                print(account['favActivity'])
                favActivity.append(int(account['favActivity']))
            else:
                for i in account['favActivity']:
                    favActivity.append(int(i))
            print(favVenue)
            # print(favActivity)
            return jsonify({'status': 'OK',
                'body':{
                    'userName':account['userName'],
                    'favActivity':favActivity,
                    'favVenue':favVenue
                }})
    else:
        return ({'status':'FAIL'})
        
# app.route("/delete_activity_organizer",methods=['POST'])
# def delete_activity_by_organizer():
#     got=request.get_json()
    
#     #deletion from the regact table
#     d_regact=db.session.query(regact).filter(regact.activityId==got['activityId']).all()
#     #print(d_regact)
#     for item in d_regact:
#         db.session.delete(item)
#         db.session.commit()
#     #deleltion from the rating table
#     d_activityRating=db.session.query(activityRating).filter(activityRating.activityId==got['activityId']).all()
#     for item in d_activityRating:
#         db.session.delete(item)
#         db.session.commit()
#         d_activities=db.session.query(Activities).filter(Activities.activityId==got['activityId']).all()
#         print(d_activities)
#     for act_item in d_activities:
#         print(act_item.activityId)
#         act_date=act_item.activityDate
#         act_time=act_item.activityTime
#         print(act_date)
#         print(act_time)
#         d_bookings=db.session.query(booking).filter(booking.venueId==act_item.activityVenueId,booking.venuedate==act_date).all()
#         print(d_bookings)
#         for book_item in d_bookings:
#             print(book_item.venueslots)
#             splitted_slots=book_item.venueslots.split(',')
#             print(splitted_slots)

#             for value in act_time:
#                 print(value)
#                 splitted_slots[value]="open/-1"
#                 print(splitted_slots)
                
#             length=len(splitted_slots)
#             list_to_string=''.join([str(elem)+',' for elem in splitted_slots[0:length-1]])

            
#             list_to_string = list_to_string + ''.join(str(splitted_slots[-1]))
#             print(list_to_string)

#             book_item.venueslots=list_to_string

#             db.session.commit()

#             #delete the activity also
#             db.session.delete(act_item)
#             db.session.commit()


#     return jsonify({'status':'OK',
#                         'body':'activitydeleted'})

@app.route("/return_participant_Details",methods=['POST'])
def participant_Details():
    got=request.get_json()
    print(got)

    p=db.session.query(regact,Accounts).filter(regact.activityId==got["activityId"]).filter(regact.userName==Accounts.userName)
    
    print(p)
    
    userNameArray=[]
    emailsArray=[]
    for item in p:
        userNameArray.append(item[0].userName)
        emailsArray.append(item[1].email)
        
    print(userNameArray)
    print(emailsArray)

    userdetails={ "userNameList":userNameArray,
                  "emailList":emailsArray}

    return jsonify({'status':'OK',
                        'body':userdetails})



@app.route("/delete_activity_organizer",methods=['POST'])
def delete_activity_by_organizer():
    got=request.get_json()
    
    #deletion from the regact table
    d_regact=db.session.query(regact).filter(regact.activityId==got['activityId']).all()
    #print(d_regact)
    for item in d_regact:
        db.session.delete(item)
        db.session.commit()

    #deleltion from the rating table
    d_activityRating=db.session.query(activityRating).filter(activityRating.activityId==got['activityId']).all()
    for item in d_activityRating:
        db.session.delete(item)
        db.session.commit()

    #deletion from the payment table
    d_activityPayment=db.session.query(activityPayment).filter(activityPayment.activityId==got['activityId']).all()
    for item in d_activityPayment:
        db.session.delete(item)
        db.session.commit()

    #deletion from the activityRating table
    d_activityRating=db.session.query(activityRating).filter(activityRating.activityId==got['activityId']).all()

    for item in d_activityRating:
        db.session.delete(item)
        db.session.commit()

    #deletion from storeimages
    d_storeimages=db.session.query(storeimages).filter(storeimages.activityId==got['activityId']).all()
    
    for item in d_storeimages:
        db.session.delete(item)
        db.session.commit()
    
    
    #updation in the venue table and then delete from the activities table
    d_activities=db.session.query(Activities).filter(Activities.activityId==got['activityId']).all()
    
    print(d_activities)
    for act_item in d_activities:
        print(act_item.activityId)
        act_date=act_item.activityDate
        act_time=act_item.activityTime
        print(act_date)
        print(act_time)
        d_bookings=db.session.query(booking).filter(booking.venueId==act_item.activityVenueId,booking.venuedate==act_date).all()
        print(d_bookings)

        for book_item in d_bookings:
            print(book_item.venueslots)
            splitted_slots=book_item.venueslots.split(',')
            print(splitted_slots)

            for value in act_time:
                print(value)
                splitted_slots[value]="open/-1"
                print(splitted_slots)
                
            length=len(splitted_slots)
            list_to_string=''.join([str(elem)+',' for elem in splitted_slots[0:length-1]])

            
            list_to_string = list_to_string + ''.join(str(splitted_slots[-1]))
            print(list_to_string)

            book_item.venueslots=list_to_string

            db.session.commit()

            #delete the activity also
            db.session.delete(act_item)
            db.session.commit()


    return jsonify({'status':'OK',
                        'body':'activitydeleted'})


@app.route("/venueopenclose",methods=['POST'])
def venuestatus():
    if request.method=="POST":
        venueId=request.json['venueId']
        venueOpen=request.json['venueOpen']
        print(venueId, venueOpen)
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("Update  venue set venueOpen=%s where venueId=%s",(venueOpen,venueId))
        mysql.connection.commit()
        return ({'status':'OK'})
    else:
        return ({'status':'FAIL'})

@app.route("/venuereviews",methods=['POST'])
def venuereviews():
    print(request.json)
    if request.method=="POST":
        venueId=request.json['venueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from venueRating where venueId=%s",(venueId,))
        data=cursor.fetchall()
        if data:
            return jsonify({'status': 'OK',
                    'body':list(data)})
        else:
            return jsonify({'status': 'OK',
                    'body':[]})
    else:
        return ({'status':'FAIL'})

@app.route("/getvenuebyowner",methods=['POST'])
def getvenuebyowner():
    if request.method=="GET":
        userName=request.json['userName']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select concat(venue.venueId,': ',group_concat(activities.activityId)) as d from venue inner join activities on venue.venueId=activities.activityVenueId where venue.venueOwner=%s group by venue.venueId",(userName,))
        data=cursor.fetchall()
        print(data)
        arr=[]
        d_val={}
        for i in data:
            venueid=i['d'].split(':')[0]
            activity_list=i['d'].split(':')[1]
            activity_list=activity_list.split(',')
            act_list_f=[]
            for i in activity_list:
                act_list_f.append(int(i))
            d_val[int(venueid)]=act_list_f
        print(d_val)
        return jsonify({'status': 'OK',

                'body':d_val})
    else:
        return ({'status':'FAIL'})

class activityPayment(db.Model):
    __tablename__="activityPayment"
    paymentId=db.Column(db.Integer,primary_key=True,nullable=False)
    activityId=db.Column(db.String(50),nullable=False)
    participantuserName=db.Column(db.String(50),nullable=False)
    organizeruserName=db.Column(db.String(50),nullable=False)
    amount=db.Column(db.Integer)

class Activities(db.Model):
    __tablename__ = "activities"
    activityId=db.Column(db.Integer,primary_key=True,nullable=False)
    activityName=db.Column(db.Text(25),nullable=False)
    activityDescription=db.Column(db.Text(25),nullable=False)
    activityCapacity=db.Column(db.Integer,nullable=False)
    activityRemainingCapacity=db.Column(db.Integer,nullable=False)
    activityLocation=db.Column(db.Text(25),nullable=False)
    activityCategory = db.Column(db.Text(25))
    activityAgeRange=db.Column(db.Text(25))
    activityCost=db.Column(db.Text(25))
    activityCostAmount=db.Column(db.Integer,nullable=False)
    activityOrganizer = db.Column(db.String(50),nullable=False)
    activityVenueId=db.Column(db.Integer,nullable=False)
    #activityVenueName= db.Column(db.String(100),nullable=False)
    #activityVenueAddress=db.Column(db.String(10),nullable=False)
    activityDate=db.Column(db.Text(20))
    activityTime=db.Column(db.JSON)# Datatype array not supported in MySql.
    #activityCity=db.Column(db.Text(25))
    #activityState=db.Column(db.Text(25))
    activityVenueCost=db.Column(db.Integer,nullable=False)
    activityBookingDate=db.Column(db.Text(100))
        
        
class Accounts(db.Model):
        __tablename__ = "accounts"
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
        

class regact(db.Model):
        __tablename__ = "regact"
        activityId=db.Column(db.Integer,ForeignKey ("activities.activityId"))
        userName=db.Column(db.Text,ForeignKey ("accounts.userName"))
        activity=relationship("Activities")
        account=relationship("Accounts")
        __mapper_args__={
            "primary_key":[activityId,userName]
        }


class venue(db.Model):
    __tablename__="venue"
    venueId=db.Column(db.Integer,primary_key=True,nullable=False)
    venueDescription=db.Column(db.String(50),primary_key=True,nullable=False)
    venueAddress=db.Column(db.String(50),nullable=False)
    venueOwner=db.Column(db.String(50),nullable=False)
    venueName=db.Column(db.String(50),nullable=False)
    # venueAvailability = db.Column(db.String(100),nullable=False)
    venueAvailability=db.Column(db.String(50),nullable=False)
    venueOpen=db.Column(db.String(10),nullable=False)
    venueHrCost=db.Column(db.Integer,nullable=False)
    venueCategory=db.Column(db.String(10),nullable=False)
    # catoryType=db.Column(db.String(50),nullable=False)
    venueCity=db.Column(db.String(50),nullable=False)
    venueState=db.Column(db.String(50),nullable=False)



class activityRating(db.Model):
    __tablename__="activityRating"
    reviewId=db.Column(db.Integer,primary_key=True)
    activityId=db.Column(db.Integer,ForeignKey ("activities.activityId"))
    userName=db.Column(db.Text,ForeignKey ("accounts.userName"))
    rating=db.Column(db.Integer)
    review=db.Column(db.Text)
    activity=relationship("Activities")
    account=relationship("Accounts")



class venueRating(db.Model):
    __tablename__="venueRating"
    reviewId=db.Column(db.Integer,primary_key=True)
    venueId=db.Column(db.Integer,ForeignKey ("venue.venueId"))
    userName=db.Column(db.Text,ForeignKey ("accounts.userName"))
    rating=db.Column(db.Integer)
    review=db.Column(db.Text)
    venue=relationship("venue")
    account=relationship("Accounts")



class booking(db.Model):
    __tablename__="booking"
    venueId=db.Column(db.Integer,ForeignKey("activities.activityVenueId"))
    venuedate=db.Column(db.String(255),ForeignKey ("venue.venueId"))
    venueslots=db.Column(db.String(255))
    __mapper_args__ = {
        "primary_key": [venueId, venuedate]
    }

class storeimages(db.Model):
    __tablename__="storeimages"
    imageId=db.Column(db.Integer,primary_key=True)
    activityId=db.Column(db.Integer,ForeignKey("activities.activityId"))
    activityImage=db.Column(db.LargeBinary)

class venueimages(db.Model):
    __tablename__="venueimages"
    imageId=db.Column(db.Integer,primary_key=True)
    venueId=db.Column(db.Integer,ForeignKey("venue.venueId"))
    venueImage=db.Column(db.LargeBinary)

UPLOAD_FOLDER = '/Users/mohitdalvi/Desktop/IUB/Software_Engg/bloomevents_files'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}


app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route("/store_image",methods=['GET','POST'])
def upload_file():
    
    # print(request['activityId'])
    print(request.args.get('activityId'))
    print(request.files.keys())
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['activityImage']
        
        print("file is",file)
        # If the user does not select a file, the browser submits an
        # empty file without a filename.
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            # file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            # return redirect(url_for('upload_file', name=filename))
            print("file in uploaded folder is"+app.config['UPLOAD_FOLDER'])

            # with open(app.config['UPLOAD_FOLDER']+"/"+filename, "rb") as img_file:
            my_string = (base64.b64encode(file.read()))
            print(my_string)

            image_obj=storeimages(
                activityId=request.args.get('activityId'),
                activityImage=my_string
            )

            db.session.add(image_obj)
            db.session.commit()

    return "imagestoredsuccessfully"

from flask import send_file
import io

@app.route("/return_image",methods=['GET'])
def return_image():
    image_stored=storeimages.query.all()
    print(image_stored)

    for item in image_stored:
        # print(type((item.pic).decode()))
    # print(base64.b64decode(storeimages.pic))
    # print(type(base64.b64decode(item.pic)))

    # retrieved_img=[{ 
    # "returned_img":base64.b64decode(storeimages.pic)
    # } for storeimages in image_stored]
        
    # return jsonify({'status':'OK',
    #                 'body':retrieved_img})
        return send_file(io.BytesIO(item.activityImage),mimetype='image/gif')
    return " "
    
    
@app.route('/venuereview', methods =['GET', 'POST'])
def venuereview():
    if request.method=="POST":
        print(request.json)
        venueId=request.json['venueId']
        userName=request.json['userName']
        rating=request.json['rating']
        review=request.json['review']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into venueRating values(%s,%s,%s,%s)",(venueId,userName,rating,review))
        mysql.connection.commit()
        return ({'status':'OK'})
    else:
        return ({'status':'FAIL'}) 

@app.route('/getvenuereview', methods =['GET', 'POST'])
def getvenuereview():
    if request.method=="GET":
        venueId=request.json['venueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select * from venueRating where venueId=%s",(venueId,))
        data=cursor.fetchall()
        if data:
            return jsonify({'status': 'OK',
                    'body':list(data)})
        else:
            return jsonify({'status': 'OK',
                    'body':[]})
    else:
        return ({'status':'FAIL'})

@app.route('/getuser', methods =['GET', 'POST'])
def getuser():
    if request.method=="POST":
        venueId=request.json['venueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        
        cursor.execute("select concat(venue.venueId,':',group_concat(activities.activityOrganizer)) as d from venue inner join activities on venue.venueId=activities.activityVenueId where venue.venueId=%s group by venue.venueId",(venueId,))
        data=cursor.fetchall()

        print(data)
        arr=[]
        d_val={}
        for i in data:
            venueid=i['d'].split(':')[0]
            activity_list=i['d'].split(':')[1]
            activity_list=activity_list.split(',')
            d_val[int(venueid)]=activity_list
        print(d_val)
        return jsonify({'status': 'OK',
                'body':d_val})
    else:
        return ({'status':'FAIL'})



stripe.api_key = 'sk_test_51LzNWXKIBfi23JtJexwSYIv4zoIRkDaQtuNf7ZM8MD18Kz5UG9lz0AB5CjuAgpGhqqhVXiJkqjKjGHk1SXHT6CPk00FJyqd39v'


def calculate_order_amount(items):
    return 1400


@app.route('/create-payment-intent', methods=['POST'])
def create_payment():
    try:
        data = json.loads(request.data)
        intent = stripe.PaymentIntent.create(
            amount=calculate_order_amount(data['items']),
            currency='usd',
            automatic_payment_methods={
                'enabled': True,
            },
        )
        return jsonify({
            'clientSecret': intent['client_secret']
        })
    except Exception as e:
        return jsonify(error=str(e)), 403

@app.route('/organisercheck', methods =['GET', 'POST'])
def organisercheck():
    if request.method=="POST":
        userName=request.json['userName']
        venueId=request.json['venueId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from activities where activityOrganizer=% s and activityVenueId=%s ', ( userName,venueId ))
        
        data=cursor.fetchone()
        if data:
            return ({'status':'OK',
            'body':"true"})
        else:
            cursor.execute('select * from venue where venueOwner=% s and venueId=%s ', ( userName,venueId ))
            d_v=cursor.fetchone()
            if d_v:
                return ({'status':'OK',
            'body':"true"})
            else:
                return ({'status':'OK',
            'body':"false"})

@app.route('/participantcheck', methods =['GET', 'POST'])
def participantcheck():
    if request.method=="POST":
        userName=request.json['userName']
        activityId=request.json['activityId']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from regact where userName=%s and activityId=%s ', ( userName,activityId ))       
        data=cursor.fetchone()
        print(userName, activityId)
        if data:
            return ({'status':'OK',
            'body':"true"})
        else:
            cursor.execute('select * from activities where activityOrganizer=% s and activityId=%s ', ( userName,activityId ))
            d_v=cursor.fetchone()
            if d_v:
                return ({'status':'OK',
            'body':"true"})

    return ({'status':'OK',
    'body':"false"})

@app.route('/authentication', methods=['POST'])
def authentication():
    if request.method=='POST':
        print(request.json['username'])
        username=request.json['username']
        a=''.join(random.choices(string.ascii_uppercase, k=16))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("insert into MFA Values(%s,%s)",(username,a))
        mysql.connection.commit()

        t=pyotp.TOTP(a)
        auth_str=t.provisioning_uri(name="Bloomevents",issuer_name='Bloomevents')
        img=qrcode.make(auth_str)
        img_io = BytesIO()
        img.save(img_io, 'PNG')
        img_io.seek(0)
        return send_file(img_io, mimetype='image/png')
    else:
        return{'status':'FAIL'}

@app.route('/MFA', methods=['POST'])
def MFA():
    
    if request.method=='POST':
        otp=request.json['otp']
        username=request.json['username']
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute("select str from MFA where username=%s",(username,))
        data=cursor.fetchone()
        str=data['str']
        print(str)
        t=pyotp.TOTP(str)
        if t.verify(otp):
            return ({'status':'OK',
            'body':"true"})
        else:
            return ({'status':'OK',
            'body':"false"})
