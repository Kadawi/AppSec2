
from flask import Flask, request, render_template, redirect, url_for, request, session, flash, g

from functools import wraps

app = Flask(__name__)

Users = {}

def checkUser(dict, key):
    if key in dict.keys():
        return false
    else:
        return true

#create new decorator to require login
def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        #adjust later for more secure sessionID
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('You need to login first.')
            return redirect(url_for('login'))
    return wrap

#secret key for establishing sessions
app.secret_key = "replaceAndMoveLater"

@app.route('/')
def home():
    ##return "Hello, world!"
    return render_template('home.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/welcome')
def welcome():
    return render_template('welcome.html')

#@app.route('/register', methods=['POST', 'GET'])
#def register():
#    if request.method == 'POST':
#        user = request.form['uname']
#        pwd = request.form['pword']
#        2fa = request.form['2fa']
        if checkKey(Users, user)
            Users{user: {'pass': pwd, '2fa': 2fa}}
        else flash('Failure')

@app.route('/login', methods=['POST', 'GET'])
def login():

    error = None
    if request.method == 'POST':
        #verify login credentials
        if request.form['uname'] != 'admin' or request.form['pword'] != 'admin':
            #return failure if incorrect credentials
            error = 'failure'
        else:
            #Set sessionID on success
            session['logged_in'] = True
            #add success message here
            flash('Success')
            #redirect to spell_check
            return redirect(url_for('home'))
    return render_template('login.html', error=error)
    

#@app.route('/spell_check', methods=['POST', 'GET'])
#@login_required

#route for logging out
#@app.route('/logout')
#@login_required
#def logout():
    #remove sessionID on logout
#    session.pop('logged_in', None)
#    flash('logged out')
    #redirect to home
#return redirect(url_for('login'))


