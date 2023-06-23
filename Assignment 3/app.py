from math import radians,sin,cos,asin,sqrt
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request
import time
import pyodbc
import redis
import hashlib
import pickle
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rudviqb'


driver = '{ODBC Driver 18 for SQL Server}'
database = 'Database02'
server = 'tcp:rb0212.database.windows.net,1433'
username = "rsb1441"
password = "Rb#azure02"


conn=pyodbc.connect('DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password)
cursor=conn.cursor()

r = redis.Redis(host='rudviq1441.redis.cache.windows.net',
                port=6379, db=0, password='GAPcGoBS3x1SGsxBZvQYZs5BZ7VpJdrZwAzCaCnUOdY=',ssl=False)

@app.route('/withredis', methods=['POST','GET'])
def redismag():
    mg1=request.form['mg1']
    mg2=request.form['mg2']
    n =int(request.form['n'])
    sql_query="Select  id,time,latitude,longitude,depth,mag,place,magType from all_month WHERE mag  between '"+mg1+"' and '"+mg2+"'"
    hash = hashlib.sha224(sql_query.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash
    t1 = time.time()
    for i in range(1,n+1):
        if(r.get(key)):
            pass
        else:
            cursor.execute(sql_query)
            data = cursor.fetchall()
            r.set(key, pickle.dumps(data))
            r.expire(key,36)
    t2 = time.time()
    time_taken=t2-t1
    return render_template("showTimeRedis.html",time2 = time_taken,no = n )   

@app.route('/withoutredis', methods=['POST','GET'])
def withoutredis():
    mg1=request.form['mg1']
    mg2=request.form['mg2']
    n =int(request.form['n'])
    sql_query="Select id,latitude,longitude,depth,mag,place,magType from all_month WHERE mag  between '"+mg1+"' and '"+mg2+"' "
    t1 = time.time()
    for i in range(1,n+1):
            cursor.execute(sql_query)
            data = cursor.fetchall()
    t2 = time.time()
    time_taken=t2-t1
    return render_template("showTimeNoRedis.html",time2 = time_taken,no = n)      

@app.route('/nrun', methods=['POST','GET'])
def nrun():
    n=int(request.form['n'])
    sql_query="Select * from all_month"
    t1 = time.time()
    for i in range(1,n+1):
            cursor.execute(sql_query)
            data = cursor.fetchall()
    t2 = time.time()
    time_taken=t2-t1
    return render_template("showTimeNoRedis.html",time2 = time_taken, no = n)      

@app.route('/nrunredis', methods=['POST','GET'])
def nrunredis():
    n=int(request.form['n'])
    sql_query="Select * from all_month"
    hash = hashlib.sha224(sql_query.encode('utf-8')).hexdigest()
    key = "redis_cache:" + hash
    t1 = time.time()
    for i in range(1,n+1):
            if(r.get(key)):
                pass
            else:
                cursor.execute(sql_query)
                data = cursor.fetchall()
                r.set(key, pickle.dumps(data))
                r.expire(key,36)
    t2 = time.time()
    time_taken=t2-t1
    return render_template("showTimeRedis.html",time2 = time_taken, no = n)        

# root 
@app.route("/", methods=['GET', 'POST'])
def index():
    return render_template('homePage.html')

@app.route('/redis')
def redis():
   return render_template('redis.html')    

@app.route('/noredis')
def noredis():
   return render_template('noredis.html')       

@app.route('/nquery')
def Nquery():
   return render_template('Nquery.html')  

@app.route('/nqueryredis')
def NqueryRedis():
   return render_template('NqueryRedis.html')  


if __name__ == '__main__':
    app.run(debug=True)
