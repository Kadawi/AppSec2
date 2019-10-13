
from flask import Flask, request, render_template, redirect, url_for, request, session, flash, g
from flask_api import status
from functools import wraps
import subprocess

app = Flask(__name__)

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
        #adjust later for more secure sessionID
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            errorMess = 'You need to login first.'
            return errorMess, status.HTTP_401_UNAUTHORIZED
    wrap.__name__ = f.__name__
    return wrap

#secret key for establishing sessions
app.secret_key = "replaceAndMaybeMoveLater"

@app.route('/')
def home():
#    ##return "Hello, world!"
#    return render_template('home.html')

    if __name__ == '__main__':
        app.run(debug=True)

    return redirect(url_for('register'))

#@app.route('/welcome')
#def welcome():
#    return render_template('welcome.html')

@app.route('/register', methods=['POST', 'GET'])
def register():
    message = None
    if request.method == 'POST':
        user = request.form['uname']
        pwd = request.form['pword']
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
        pwd = request.form['pword']
        mfa = request.form['2fa']
        if (not (checkUser(Users, user))):
            error = 'Incorrect'
        elif pwd != Users[user]['pass']:
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
        check = subprocess.run(["./a.out", txt, 'wordlist.txt'], stdout=subprocess.PIPE,)
        misspelled = check.stdout
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


