import pyodbc
from flask import Flask, render_template, request

app = Flask(__name__)

#To route to home page
@app.route('/')
def toHome():
   return render_template('homepage.html')

#To route to the webpage for entering users name for searching
@app.route('/search_name')
def search():
   return render_template('search_name.html')

#To route to update page   
@app.route('/updatekeyword')
def updatemain():
   return render_template('updatekey.html')

#To route to update salary page   
@app.route('/changeSal')
def updatemainsal():
   return render_template('changeSal.html')

#To route to delete page
@app.route('/deleterec')
def deletemain():
   return render_template('delete_rec.html')

#To route to salary range page
@app.route('/salrng')
def checksalrange():
   return render_template('chkSalRange.html')

#To route to addpicture page
@app.route('/addImage')
def addImg():
   return render_template('addImage.html')

#To connect the database and user credentials to Microsoft Azure
driver = '{ODBC Driver 18 for SQL Server}'
database = 'Database02'
server = 'tcp:rb0212.database.windows.net,1433'
username = "rsb1441"
password = "Rb#azure02"
conn= pyodbc.connect('DRIVER='+driver+';SERVER='+server+';DATABASE='+database+';UID='+username+';PWD='+ password)
cursor = conn.cursor() #cursor

#To search the record from the table by using name
@app.route('/searchuser', methods=['POST','GET'])
def list():
    field=str(request.form['name'])
    querry="Select * from q1c WHERE Name ='"+field+"' "
    cursor.execute(querry)
    rows = cursor.fetchall()
    return render_template("getImage.html",rows = rows)

#To check the word availability in list
@app.route('/searchuser', methods=['POST','GET'])
def list():
    field=str(request.form['name'])
    querry="SELECT * from test where charm like LIKE :charm"
    cursor.execute(querry,{"charm": '%' + field + '%'})
    rows = cursor.fetchall()
    return render_template("getImage.html",rows = rows)

#To retrieve all the data from table
@app.route('/showList', methods=['POST','GET'])
def fulllist():
    querry="Select * from q1c "
    cursor.execute(querry)
    rows = cursor.fetchall()
    return render_template("completeList.html",rows = rows)

#To update keyword of the record from the table by using name
@app.route('/key_update',methods=['POST','GET'])
def update():
    if (request.method=='POST'):
        name= str(request.form['name'])
        keyword= str(request.form['keyword'])
        querry="UPDATE q1c SET keywords = '"+keyword+"'   WHERE Name ='"+name+"' "
        cursor.execute(querry)
        conn.commit()
        querry2="Select * from q1c "
        cursor.execute(querry2)
        rows = cursor.fetchall()
    return render_template("completeList.html",rows = rows)

#To add picture to the record from the table by using name
@app.route('/addImg',methods=['POST','GET'])
def addpicture():
    if (request.method=='POST'):
        name= str(request.form['name1'])
        pic= str(request.form['pic1'])
        querry="UPDATE q1c SET Picture = '"+pic+"'   WHERE Name ='"+name+"' "
        cursor.execute(querry)
        conn.commit()
        querry2="Select * from q1c "
        cursor.execute(querry2)
        rows = cursor.fetchall()
    return render_template("completeList.html",rows = rows)

#To update salary of the record from the table by using name
@app.route('/salaryupdate',methods=['POST','GET'])
def chnagesal():
    if (request.method=='POST'):
        name= str(request.form['name'])
        keyword= str(request.form['sal'])
        querry="UPDATE q1c SET salary = '"+keyword+"'   WHERE Name ='"+name+"' "
        cursor.execute(querry)
        conn.commit()
        querry2="Select * from q1c "
        cursor.execute(querry2)
        rows = cursor.fetchall()
    return render_template("completeList.html",rows = rows)

#To delete the record from the table by using name
@app.route('/recdelete', methods=['GET', 'POST'])
def deleterecord():
    if (request.method=='POST'):
        name= str(request.form['name'])
        querry="DELETE FROM q1c WHERE Name ='"+name+"' "
        cursor.execute(querry)
        conn.commit()
        querry2="Select * from q1c "
        cursor.execute(querry2)
        rows = cursor.fetchall()
    return render_template("completeList.html",rows = rows)

#To retrieve the record which is in the given range from the table by using max and min salary
@app.route('/sal', methods=['GET', 'POST'])
def notmatch():
    if (request.method=='POST'):
        salrange= (request.form['range'])
        querry="select * from q1c WHERE Salary  <'"+salrange+"'"
        cursor.execute(querry)
        rows = cursor.fetchall()
    return render_template("getImage.html",rows = rows)

if __name__ =="__main__":
    app.run(debug=True)
    