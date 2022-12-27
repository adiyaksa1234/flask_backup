from flask import Flask, render_template, url_for, request, redirect, session, abort, jsonify, flash
from flask_mysqldb import MySQL
import MySQLdb.cursors
import re
import os
import json
from datetime import timedelta
from flask_toastr import Toastr
import time
import threading
import requests

json_open = open('connect.json')

data = json.load(json_open)

app = Flask(__name__)

toastr = Toastr(app)

app.secret_key = os.urandom(30)

app.config["MYSQL_HOST"] = data['host']
app.config["MYSQL_USER"] = data['user']
app.config["MYSQL_PASSWORD"] = data['password']
app.config["MYSQL_DB"] = data['database']

app.config["SESSION_TYPE"] = "filesystem"

mysql = MySQL(app)

@app.before_request
def before_request():
    if 'loggedin' not in session or not session.get('loggedin'):
        return login_web()

@app.route('/')
def home():
    flash({'title': "Welcome", 'message': "Hei selamat datang dipanel mysql flask"}, 'info')    
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login_web():   
    if 'loggedin' not in session or not session.get('loggedin'):
        title = "Login Panel"
        if request.method == 'POST':
            username = request.form.get('username')
            password = request.form.get('password')
            # recaptcha_response = request.form['g-recaptcha-response']
            # url = 'https://www.google.com/recaptcha/api/siteverify'
            # values = {
            #     'secret': '6LfRlYojAAAAAMSaghF3tjxhEHXeivPrSDM0hLyZ',
            #     'response': recaptcha_response
            # }
            # response = requests.post(url, data=values)
            # result = response.json()
            remember_me = request.form.get('remember_me')
            cr = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cr.execute("SELECT * FROM user WHERE username= %s AND password=PASSWORD(%s)", (username, password, ))
            account = cr.fetchone()
            # if result['success']:
            if account:
                        session['id'] = account['id']
                        session['username'] = account['username']
                        session['loggedin'] = True
                        if remember_me:
                                os.system("cls")
                                print("[DEBUG] User mengklik remember me")
                                app.permanent_session_lifetime = timedelta(days=30)
                                print(app.permanent_session_lifetime)
                                session.permanent = True
                        else:
                                os.system("cls")
                                print("[DEBUG] User tidak mengklik remember me")
                                app.permanent_session_lifetime = timedelta(hours=6)
                                print(app.permanent_session_lifetime)
                                session.permanent = False
                        return home()
            else: 
                    flash({'title': "Invalid", 'message': "Username/password salah"}, 'error')    
            # else:
            #  flash({'title': "Invalid", 'message': "Harap klik recaptcha / tombol im not robot"}, 'error')  
    else:
        return redirect(url_for('home'))
   
    return render_template('login.html', title = title)

@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for('login_web'))

if __name__ == "__main__":
   app.run(debug=True, port=80)
