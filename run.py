import psycopg2
from flask import Flask, render_template
app = Flask(__name__)
con = psycopg2.connect(host='localhost',dbname='profile', user='postgres', password='12345', port='5432')
cursor = con.cursor()

@app.route("/", methods=['post', 'get'])
def test():  
    #cursor.execute("select * from cart")
    #result = cursor.fetchall()
    #return render_template("test.html", data=result)
    return('<h1>Welcome</h1>')


if __name__=="__main__":
    app.run(host="localhost",port=int('5002'))
    