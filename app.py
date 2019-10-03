
m flask import Flask, request
app = Flask(__name__)

@app.route('/')
def something():
    something

if __name__ == '__main__':
    app.run()

@app.route('/register', methods=['POST', 'GET'])
def register():
    if request.method == 'POST':
        user = request.form['username']
        pwd = request.form['password']
        other stuff
    if request.method == 'GET':
        #serve them the registration page

@app.route('/login', methods['POST', 'GET'])

@app.route('/spell_check', methods=['POST', 'GET'])


