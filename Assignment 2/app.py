from math import radians,sin,cos,asin,sqrt
from datetime import date, datetime, timedelta
from flask import Flask, render_template, request
import pyodbc
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



with pyodbc.connect(
        'DRIVER=' + driver + ';SERVER=' + server + ';PORT=1433;DATABASE=' + database + ';UID=' + username + ';PWD=' + password) as conn:
    with conn.cursor() as cursor:
        temp = []
        cursor.execute("SELECT TOP 3 time, id FROM earthquake")
        while True:
            r = cursor.fetchone()
            if not r:
                break
            print(str(r[0]) + " " + str(r[1]))
            temp.append(r)


@app.route("/", methods=['GET', 'POST'])
def toHome():
    return render_template('homePage.html')


class showMag(FlaskForm):
    mag = StringField(label='Enter the Magnitude: ', validators=[DataRequired()])
    submit = SubmitField(label='Submit')


@app.route('/magcount', methods=['GET', 'POST']) 
def magcount():
    form = showMag()
    cnt = 0
    if form.validate_on_submit():
        try:
            magcount = float(form.mag.data)
            if magcount <= 5.0:
                return render_template('displayMag.html', form=form, error="value must be > 5.0", temp=1)
            cursor.execute("SELECT * FROM earthquake where mag > ?", magcount)
            output = []
            while True:
                row = cursor.fetchone()
                if not row:
                    break
                output.append(row)
                cnt += 1
            return render_template('displayMag.html', output=output, cnt=cnt, temp=0)
        except ValueError:
            return render_template('displayMag.html', form=form, error="value must be numeric.", temp=1)
    return render_template('displayMag.html', form=form, temp=1)

def distance(lat1, lat2, lon1, lon2):
	lon1 = radians(lon1)
	lon2 = radians(lon2)
	lat1 = radians(lat1)
	lat2 = radians(lat2)
	# Haversine formula
	dlon = lon2 - lon1
	dlat = lat2 - lat1
	a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
	c = 2 * asin(sqrt(a))
	# Radius of earth in kilometers. Use 3956 for miles
	r = 6371
	# calculate the result
	return(c * r)

@app.route('/specLoc',methods=['POST','GET'])
def lsearch():
    if request.method =='POST':
        lat1=request.form['lat1']
        lon1=request.form['lon1']
        km=request.form['kms']
        querry="Select id,time,latitude,longitude,mag,place from earthquake"
        cursor.execute(querry)
        lat1=float(lat1)
        lon1=float(lon1)
        km=float(km)
        rows = cursor.fetchall()
        bkm=[]
        for i in rows:
            x=distance(lat1,float(i[2]),lon1,float(i[3]))
            if x<=km:
                bkm.append(i)
        return render_template("specLoc.html",rows = bkm)
    else:
        return render_template('specLoc.html')    

@app.route('/magRange', methods = ['GET','POST'])
def magRange():
    if request.method =='POST':
        Range1 = str(request.form['Range1'])
        Range2 = str(request.form['Range2'])
        Fromdate = request.form['Fromdate']
        Todate = request.form['Todate']
        query = "SELECT * FROM dbo.earthquake where (mag BETWEEN '"+Range1+"' and '"+Range2+"') and (CAST(time as date) BETWEEN CAST('"+Fromdate+"' as date) and CAST('"+Todate+"' as date)) "
        cursor.execute(query)
        results = cursor.fetchall()
        return render_template("magRange.html", length = len(results), rows = results,temp=0)
    else:
        return render_template("magRange.html",temp=1)


@app.route("/clust", methods=['GET', 'POST'])
def cluster():
    count =0
    query=("SELECT mag,COUNT(*) FROM earthquake  group by mag")
    cursor.execute(query)
    result=cursor.fetchall()
    return render_template("cluster.html",msg="completed", rows=result)

@app.route('/nightNDay',methods=['POST','GET'])
def nightdata():
    count=0
    time1 = "06:00:00.0000000 +00:00"
    time2 = "18:00:00.0000000 +00:00"
    query = "SELECT place, CAST(time as time) FROM dbo.earthquake where mag > 4.0 and (CAST(time as time) not BETWEEN CAST('"+time1+"' as time) and CAST('"+time2+"' as time)) "
    cursor.execute(query)
    result = cursor.fetchall()
    count1 = len(result)
    query1 = "SELECT place, CAST(time as time) FROM dbo.earthquake where mag > 4.0"
    cursor.execute(query1)
    result1 = cursor.fetchall()
    count2 = len(result1)

    if(count1>(count2-count1)):
        display="Earthqakes occur more at night(6pm to 6am) than in the day,out of "+str(count2)+" earth quakes "+str(count1)+" occured in the night"
    else:
        display="Earthqakes occur more at day(6am to 6pm) than in the night,out of "+str(count2)+" earth quakes "+str(count2-count1)+" occured in the day time"
    return render_template("newrecord.html",display = display)              

if __name__ == '__main__':
    app.run(debug=True)
