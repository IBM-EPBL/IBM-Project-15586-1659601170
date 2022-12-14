from flask import Flask,render_template,request,url_for,redirect,session
import ibm_db
import os
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import requests

app=Flask(__name__)
app.secret_key='a'
try:
    dsn_hostname = "1cbbb1b6-3a1a-4d49-9262-3102a8f7a7c8" 
    dsn_uid = "gvv70240"
    dsn_pwd = "4v3lxGOm5WdcKOc7"
    dsn_driver = "{IBM DB2 ODBC DRIVER}"
    dsn_database = "bludb"
    dsn_port = "32459"
    dsn_protocol = "TCPIP"
    dsn = (
    "DRIVER={0};"
    "DATABASE={1};"
    "HOSTNAME={2};"
    "PORT={3};"
    "PROTOCOL={4};"
    "UID={5};"
    "PWD={6};").format(dsn_driver, dsn_database, dsn_hostname, dsn_port, dsn_protocol, dsn_uid, dsn_pwd)
    print (dsn)
    conn=ibm_db.connect(dsn, 'gvv70240', '4v3lxGOm5WdcKOc7')
    print ("Connected to database:" , dsn_database,"as user: ", dsn_uid, "on host: ", dsn_hostname)
    # conn=ibm_db.connect("DATABASE=bludb;HOSTNAME=ba99a9e6-d59e-4883-8fc0-d6a8c9f7a08f.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;PORT=31321;SECURITY=SSL;SSLServerCertificate=DigiCertGlobalRootCA.crt;UID=gkr16989;PWD=WvN7xr79Kp6YfdL7","","")
    # conn=ibm_db.connect('DATABASE=1cbbb1b6-3a1a-4d49-9262-3102a8f7a7c8;'
    #                  'HOSTNAME=9938aec0-8105-433e-8bf9-0fbb7e483086.c1ogj3sd0tgtu0lqde00.databases.appdomain.cloud;'  
    #                  'PORT=32459'
    #                  'PROTOCOL=TCPIP;'
    #                  'UID=gvv70240;'
    #                  'PWD=4v3lxGOm5WdcKOc7;', 'gvv70240', '4v3lxGOm5WdcKOc7')
except:
    print("Unable to connect: ",ibm_db.conn_error())
  

@app.route("/")
def home():
    session['status_msg']=' '
    
    return render_template('Home.html')

@app.route("/reg")
def reg():
    return render_template('Registration.html')

@app.route("/register",methods=["POST","GET"])
def register():
     if request.method == 'POST' :
        firstName = request.form['firstName']
        lastName = request.form['lastName']
        
        session['email'] = request.form['email']
        phoneNumber = request.form['phoneNumber']
        password = request.form['password']
        sql = "SELECT * FROM registration WHERE EMAIL_ID=?"
        stmt = ibm_db.prepare(conn, sql)
        ibm_db.bind_param(stmt,1,session['email'])
        ibm_db.execute(stmt)
        account = ibm_db.fetch_assoc(stmt)
        print(account)
        message = Mail(from_email='nutriaux04@gmail.com',to_emails=session['email'],subject="NutriAux - Registration",html_content='<b>NutriAux welcomes you</b><br/><p>Your account has been registered successfully</p>')
        try:
            sg=SendGridAPIClient('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')
            response=sg.send(message)
            print(response.status_code)
            print(response.body)
            print(response.headers)
        except Exception as e:
            print(e)
        
        
        if account:
            
            
            session['status_msg']= 'Account already exists ! Kindly login'
            return redirect(url_for('login'))
        else :
            insert_sql = "INSERT INTO registration VALUES (?,?,?,?,?)"
            prep_stmt = ibm_db.prepare(conn, insert_sql)
            ibm_db.bind_param(prep_stmt, 1, firstName)
            ibm_db.bind_param(prep_stmt, 2, lastName)
            ibm_db.bind_param(prep_stmt, 3, session['email'])
            ibm_db.bind_param(prep_stmt, 4, phoneNumber)
            ibm_db.bind_param(prep_stmt, 5, password)
            ibm_db.execute(prep_stmt)
        print('You have successfully registered !')
        return redirect(url_for('personaldetails'))
    



@app.route("/personaldetails")
def personaldetails():
    return render_template("personaldetails.html")

@app.route("/addpersonaldetails",methods=["POST","GET"])
def addpersonaldetails():
    if request.method == 'POST' :
        age=float(request.form.get('age'))
        gender=request.form.get('Gender')
        weight=float(request.form.get('weight'))
        height=float(request.form.get('height'))
        activity=request.form.get('activity')
        print(age,gender,weight,height,activity)
        if(gender == 'male'and activity == "1"):
            totalCalories = 1.2 * (66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age))
        elif(gender == 'male' and activity == "2"):
            totalCalories = 1.375 * (66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age))
        elif (gender == 'male' and activity == "3"):
            totalCalories = 1.55 * (66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age))
        elif(gender == 'male' and activity == "4"):
            totalCalories = 1.725 * (66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age))
        elif(gender == 'male' and activity == "5"): 
            totalCalories = 1.9 * (66.5 + (13.75 * weight) + (5.003 * height) - (6.755 * age))
        elif(gender == 'female' and activity == "1"):
            totalCalories = 1.2 * (655 + (9.563 * weight) + (1.850 * height) - (4.676 * age))
        elif(gender == 'female' and activity == "2"):
            totalCalories = 1.375 * (655 + (9.563 * weight) + (1.850 * height) - (4.676 * age))
        elif(gender == 'female' and activity == "3"):
            totalCalories = 1.55 * (655 + (9.563 * weight) + (1.850 * height) - (4.676 * age))
        elif(gender == 'female' and activity == "4"):
            totalCalories = 1.725* (655 + (9.563 * weight) + (1.850 * height) - (4.676 * age))
        else: 
            totalCalories = 1.9 * (655 + (9.563 * weight) + (1.850 * height) - (4.676 * age))
        print(int(totalCalories))
        BMI = (weight / (height/100)**2 )
        if BMI <= 18.5:  
            BMI_message="underweight"  
        elif BMI <= 24.9:  
            BMI_message="healthy"  
        elif BMI <= 29.9:  
            BMI_message="overweight"
        else:
            BMI_message="obese"   
        print(BMI)
        insert_query="INSERT INTO personal_details VALUES(?,?,?,?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_query)
        ibm_db.bind_param(prep_stmt,1,session['email'])
        ibm_db.bind_param(prep_stmt,2,str(int(age)))
        ibm_db.bind_param(prep_stmt,3,gender)
        ibm_db.bind_param(prep_stmt,4,str(weight))
        ibm_db.bind_param(prep_stmt,5,str(height))
        ibm_db.bind_param(prep_stmt,6,str(totalCalories))
        ibm_db.bind_param(prep_stmt,7,str(BMI))
        ibm_db.execute(prep_stmt)
    return redirect(url_for('login'))


@app.route("/login")
def login():
    return render_template("login.html",message=session['status_msg'])


@app.route("/verify",methods=["POST","GET"])
def verify():
    session['email'] = request.form.get("email")
    password = request.form.get("password")
    get_query="SELECT * FROM registration WHERE EMAIL_ID=? AND PASSWORD=?"
    prep=ibm_db.prepare(conn,get_query)
    ibm_db.bind_param(prep,1,session['email'])
    ibm_db.bind_param(prep,2,password)
    result=ibm_db.execute(prep)
    login = ibm_db.fetch_assoc(prep)
    if login:
        get_query="SELECT weight,height,daily_calorie_intake,BMI FROM personal_details WHERE EMAIL_ID=?"
        prep=ibm_db.prepare(conn,get_query)
        ibm_db.bind_param(prep,1,session['email'])
        result=ibm_db.execute(prep)
        data = ibm_db.fetch_tuple(prep)
        global weight  
        weight= data[0]
        global height 
        height= data[1]
        global daily_calorie_intake
        daily_calorie_intake=data[2]
        daily_calorie_intake=daily_calorie_intake[0:7]
        global BMI
        BMI=data[3]
        BMI=BMI[0:4]
        return redirect((url_for('dashboard')))
    print("Wrong password" , session['email'],password)
    return render_template("login.html",message="Incorrect Email ID or Password! Try again")

@app.route("/dashboard")
def dashboard():
    return render_template('dashboard.html',weight=weight,height=height,daily_calorie_intake=daily_calorie_intake,BMI=BMI)
   
@app.route("/upload")
def upload():
    return render_template('upload.html',calories="",fat="",protein="",carbs="")



@app.route("/history")
def history():
    get_query="SELECT CHAR(DATE_OF_CONSUMPTION,EUR)AS DATE,MEAL_NAME,CALORIES FROM TRACKHISTORY WHERE EMAIL_ID=?"
    prep=ibm_db.prepare(conn,get_query)
    ibm_db.bind_param(prep,1,session['email'])
    result=ibm_db.execute(prep)
    if result==False:
        print("not working")
    history=[]
    dictionary = ibm_db.fetch_assoc(prep)
    while dictionary != False:
        history.insert(0,dictionary["DATE"])
        history.insert(1,dictionary["MEAL_NAME"])
        history.insert(2,dictionary["CALORIES"])
      
        print("The date is : ", dictionary["DATE"])
        print("The name is : ", dictionary["MEAL_NAME"])
        print("The calories is : ", dictionary["CALORIES"])
        dictionary = ibm_db.fetch_assoc(prep)
    print(history) 
    no_of_rows=len(history)//3
    print(no_of_rows) 
    return render_template("History.html",history=history,no_of_rows=no_of_rows)


@app.route("/addhistory",methods=["POST","GET"])
def addhistory():
    if request.method=='POST':
        date=request.form['date']
        meal_name=request.form['meal_name']
        calories=request.form['calories']
        insert_query="INSERT INTO trackhistory VALUES(?,?,?,?)"
        prep_stmt=ibm_db.prepare(conn,insert_query)
        ibm_db.bind_param(prep_stmt,1,session['email'])
        ibm_db.bind_param(prep_stmt,2,date)
        ibm_db.bind_param(prep_stmt,3,meal_name)
        ibm_db.bind_param(prep_stmt,4,calories)
        ibm_db.execute(prep_stmt)
    
    return redirect(url_for('history'))
        

@app.route("/support")
def support():
    return render_template("support.html")

if __name__ == '__main__':
    app.run(debug=True)