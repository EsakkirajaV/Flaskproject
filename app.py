from flask import Flask,render_template,request,session,redirect,url_for
#from flask_mysqldb import MySQL
#import MySQLdb.cursors
import psycopg2
import re



app = Flask(__name__)

app.secret_key='\xfd{H\xe5<\x95\xf9\xe3\x96.5\xd1\x01O<!\xd5\xa2\xa0\x9fR"\xa1\xa8'

app.debug = True

con = psycopg2.connect(host='localhost',dbname='profile', user='postgres', password='12345', port='5432')
cursor = con.cursor()
#app.config['MYSQL_HOST']='localhost'
#app.config['MYSQL_USER']='root'
#app.config['MYSQL_PASSWORD']=''
#app.config['MYSQL_DB']='profile'

#mysql = MySQL(app)

@app.route('/')
@app.route('/login', methods =['GET', 'POST'])
def login():
    msg = ""
    if request.method=='POST' and 'username' in request.form and 'password' in request.form:
        username = request.form['username']
        password = request.form['password']
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accounts where username= %s and password = %s',(username,password,))
        account = cursor.fetchone()
        if account:
            print(account)
            session['loggedin']= True
            session['id'] = account[0] 
            session['username'] = account[1]
            msg = 'Logged in successfully'
            return render_template("index.html",msg = msg)
        else:
            msg = 'Incorrect username / Password !'   
            return render_template("login.html", msg = msg) 
    return render_template("login.html", msg = msg)

@app.route('/register', methods=['GET', 'POST'])
def register():
    msg =" "
    if request.method=="POST":
        username = request.form['username']
        password = request.form['password']
        email    = request.form['email']
        organisation = request.form['organisation']
        address = request.form['address']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        postalcode = request.form['postalcode']
        #cursor =   mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accounts where username= %s', (username, ))
        account=cursor.fetchone()
        if account:
            msg = 'Accounts Already exists'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            msg = 'Invalid email address !'
        elif not re.match(r'[A-Za-z0-9]+', username):
            msg = 'name must contain only characters and numbers !'
        else:
            cursor.execute('INSERT INTO accounts VALUES (NULL, %s,%s,%s,%s,%s,%s,%s,%s,%s)',(username,password,email,organisation,address,city,state,country,postalcode,))
            #mysql.connection.commit()
            cursor.commit()
            msg = 'You have sucessfully registered'

        return(render_template("register.html",msg=msg))
    else:    
        return(render_template("register.html",msg=msg))
@app.route('/index')
def index():
    if 'loggedin' in session:
        return render_template("index.html")
    return redirect(url_for('login'))

@app.route('/display')
def display():
    if 'loggedin' in session:
        #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursor.execute('select * from accounts')
        accounts = cursor.fetchall()
        return render_template('display.html',accounts=accounts)

    return redirect(url_for('login'))

@app.route('/edit/<id>', methods=["GET","POST"])
def edit(id):
    if 'loggedin' in session:
        if id:
            #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from accounts where id =%s',(id),)
            account = cursor.fetchone()
            print(account)
            return render_template('update.html',account=account)
    else:
        return redirect('login')
@app.route('/update/<int:account_id>', methods=['GET','POST'])
def update(account_id):
    #print('come in')
    #print(request.form)
    if 'loggedin' in session:
        msg =''
        if request.method=='POST':
            username = request.form['username']
            password = request.form['password']
            email    = request.form['email']
            organisation = request.form['organisation']
            address = request.form['address']
            city = request.form['city']
            state = request.form['state']
            country = request.form['country']
            postalcode = request.form['postalcode']

            #cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursor.execute('select * from accounts where username = %s',(username,))
            account = cursor.fetchone()
            if account:
                cursor.execute('update accounts SET username = %s, password =%s, email =%s, organisation =%s, address =%s, city =%s, state =%s, country =%s, postalcode =%s WHERE id =%s', (username,password,email,organisation,address,city,state,country,postalcode, (session['id'], ), ))
                #mysql.connection.commit()
                cursor.commit()
                msg = 'Updated Successfully'
            else:
                cursor.execute('update accounts SET username = %s, password =%s, email =%s, organisation =%s, address =%s, city =%s, state =%s, country =%s, postalcode =%s WHERE id =%s', (username,password,email,organisation,address,city,state,country,postalcode, (session['id'], ), ))
                #mysql.connection.commit()
                cursor.commit()
                msg = 'Updated Successfully'
        return redirect(url_for('display'))          
    return redirect(url_for('login'))                



@app.route('/logout')
def logout():
    session.pop('loggedin',None)
    session.pop('id',None)
    session.pop('username',None)
    return redirect(url_for('login'))
if __name__== "__main__":
     app.run(host="localhost",port=int("5001"))