from email.message import Message
from flask_cors import CORS
import uuid
from flask import Flask, render_template, request, redirect, url_for
from flask import Flask, session
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
from flask_mail import Mail, Message
# from init import mail

app = Flask(__name__)
mail= Mail(app)
CORS(app)
app.secret_key = 'your secret key'
app.config['MYSQL_HOST'] = '127.0.0.1'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = 'Alok321#'
app.config['MYSQL_DB'] = 'sys'


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
    msg = ''
    if request.method == 'POST' and 'userName' in request.json and 'password' in request.json:
        username = request.json['userName']
        pas = request.json['password']
        password=str(hash(pas))
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s AND pass = % s', (username, password, ))
        account = cursor.fetchone()
        if account:
            session["username"]=account["username"]
            msg = 'Logged in successfully !'
            return "OK"
            # return render_template('index.html', msg = msg)
        else:
            return "FAIL"
    
 
@app.route('/logout',methods =['GET', 'POST'])
def logout():
    session.pop('loggedin', None)
    session.pop('id', None)
    session.pop('username', None)
    return "LOGGED_OUT"
 
@app.route('/register', methods =['GET', 'POST'])
def register():
    msg = ''
    if request.method == 'POST' and 'firstName' in request.json and 'lastName' in request.json and 'userName' in request.json and 'password' in request.json and 'email' in request.json  and 'isOwner' in request.json:
        first_name = request.json['firstName']
        last_name = request.json['lastName']
        username = request.json['userName']
        pas = request.json['password']
        password=str(hash(pas))
        email = request.json['email']
        owner=request.json['isOwner']
        token=""
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE username = % s', (username, ))
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
            msg = 'OK'
    elif request.method == 'POST':
        msg = 'FAIL_R'
    return msg

@app.route('/reset_mail', methods =['GET', 'POST'])
def reset():
    if request.method == 'POST' and 'email' in request.json:
        email = request.json['email']
        token=str(uuid.uuid4())
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE email = % s', (email, ))
        account = cursor.fetchone()
        if account:
            msg=Message("Forget your password", sender="eventabloom@gmail.com",recipients=[email])
            msg.body="heyyyyyyyyyy babyyyyyyyyyyyyyyyyyyyyyy"
            mail.send(msg)
            cursor.execute('Update accounts SET token= %s WHERE email = % s', (token,email,))
            mysql.connection.commit()
            return "OK"
        else:
            return "FAIL"

@app.route('/password_reset/<token>', methods =['GET', 'POST'])
def pass_reset(token):
    if request.method == 'POST' and 'password' in request.json:
        password = request.json['password']
        token1=str(uuid.uuid4())
        cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('SELECT * FROM accounts WHERE token = % s', (token, ))
        account = cursor.fetchone()
        if account:
            cursor.execute('Update accounts SET token= %s, pass= %s WHERE token = % s', (token1,password,token,))
            mysql.connection.commit()
            return "OK"
        else:
            return "FAIL"
    