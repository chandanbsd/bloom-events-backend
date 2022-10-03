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
    