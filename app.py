
from flask import Flask, request, render_template, redirect, url_for, request, session, flash, g
from flask_api import status
from functools import wraps
from flask_wtf.csrf import CSRFProtect
import subprocess
import os
from passlib.hash import sha256_crypt, pbkdf2_sha256

app = Flask(__name__)

app.config.from_object('config.DefaultConfig')

Users = {}

def checkUser(dict, key):
    if key in dict.keys():
        return True
    else:
        return False

#create new decorator to require login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            errorMess = 'You need to login first.'
            return errorMess, status.HTTP_401_UNAUTHORIZED
    wrap.__name__ = f.__name__
    return wrap

#random secret key 
app.secret_key = os.urandom(64)
csrf = CSRFProtect(app)

@app.route('/')
def home():

    if __name__ == '__main__':
        app.run()


    return redirect(url_for('register'))

@app.route('/register', methods=['POST', 'GET'])
def register():
    message = None
    if request.method == 'POST':
        user = request.form['uname']
        pwd = pbkdf2_sha256.hash(request.form['pword'])
        #pwd = request.form['pword']
        mfa = request.form['2fa']
        if (not (checkUser(Users, user))):
            Users[user] = {}
            Users[user] = {'pass': pwd, 'twofa': mfa}
            message = "success"

        else:
            message = "failure"
            #flash('Failure')
    return render_template('register.html', message=message)

@app.route('/login', methods=['POST', 'GET'])
def login():

    error = None
    if request.method == 'POST':
        #verify login credentials
        user = request.form['uname']
        #pwd = sha256_crypt.encrypt(request.form['pword'])
        pwd = request.form['pword']
        mfa = request.form['2fa']
        if (not (checkUser(Users, user))):
            error = 'Incorrect'
        elif not(pbkdf2_sha256.verify(str(pwd), str(Users[user]['pass']))):
        #elif pwd != Users[user]['pass']:
            error = 'Incorrect'
        elif mfa != Users[user]['twofa']:
            error = "Two-factor failure"
        else:
            #Set sessionID on success
            session['logged_in'] = True
            #add success message here
            error = 'success'
    return render_template('login.html', error=error)
    

@app.route('/spell_check', methods=['POST', 'GET'])
@login_required
def spell_check():
    misspelled = None
    txt = None
    if request.method == 'POST':
        txt = request.form['inputtext']
        with open("input.txt", "w") as f:
            f.write(txt)
        check = subprocess.run(["./a.out", "input.txt", 'wordlist.txt'], stdout=subprocess.PIPE,)
        misspelled = check.stdout.decode('utf-8')
        misspelled.replace("\n",", ")
    return render_template('spell_check.html', txt=txt, misspelled=misspelled)

#route for logging out
@app.route('/logout')
@login_required
def logout():
    #remove sessionID on logout
    session.pop('logged_in', None)
    flash('logged out')
    #redirect to home
    return redirect(url_for('login'))


