import os
import numpy as np #used for numerical analysis
from flask import Flask,request,render_template,flash,redirect,url_for# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
#render_template- used for rendering the html pages
from tensorflow.keras.models import load_model#to load our trained model
from tensorflow.keras.preprocessing import image
import sqlite3
from sqlite3 import Error
from flask_mail import Mail, Message

import smtplib , getpass

#for single email
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

app=Flask(__name__, template_folder='template/HTML')#our flask app
model=load_model(r'color_1.h5')#loading the model

#configuration the mail
app.secret_key = "abc"  
#app.config["MAILSERVER"] = 'smtp.gmail.com'
#app.config["MAIL_PORT"] = 465      
#app.config["MAIL_USERNAME"] = 'username@gmail.com'  
#app.config['MAIL_PASSWORD'] = '*************' 
#app.config["MAIL_USERNAME"] = 'teamfashionera04@gmail.com'  
#app.config['MAIL_PASSWORD'] = 'FashionEra@1289'  
#app.config['MAIL_USE_TLS'] = False  
#app.config['MAIL_USE_SSL'] = True 
#mail = Mail(app)

EMAIL_ID = "teamfashionera04@gmail.com"
PASSWORD = "FashionEra@1289"
SMTP_PORT = 587

s = smtplib.SMTP(host='smtp.gmail.com', port=SMTP_PORT)
s.starttls()
s.login(EMAIL_ID,PASSWORD)

@app.route("/",methods=['GET','POST']) #default route
def intro():
    return render_template("intro_page.html")#rendering html page

@app.route("/about_page") 
def about():
	return render_template("about_page.html")#rendering html page

@app.route("/help_page") 
def help():
	return render_template("help_page.html")#rendering html page

@app.route("/login_page",methods=['GET','POST'])
def login():
    database = r"C:\IBM Hack Challenge\database.db"
    conn = connection(database)
    if request.method=='POST':
        UserName = request.form['username']
        PWD = request.form['password']
        print(UserName)
        print(PWD)
        rows=0
        cur = conn.cursor()
        cur.execute("Select * from User_Data where UserName = ? and PWD = ?",(UserName,PWD,))
        rows = cur.fetchall()
        for row in rows:
            print("\n*Personal Details*\nName:",row[1],"\nEmail: ",row[2],"\n\n*Address Details*\nAddress:",row[3],"\nDOB:",row[4],"\n\n*Contact Details*\nMobile:",row[5],"\nPrivate_Key:",row[8])
            if rows is None:
                return render_template("login_page.html")
            else:
                return render_template("main_page.html")
	
    return render_template("login_page.html")

@app.route("/forgot_page",methods=['GET','POST']) 
def forgot_page():
    database = r"C:\IBM Hack Challenge\database.db"
    conn = connection(database)
    if request.method=='POST':
        PWD = 11
        Email = request.form['Email']
        Private_key = request.form['private_key']
        print(Email)
        print(Private_key)
        rows=0
        cur = conn.cursor()
        cur.execute("Select * from User_Data where Email = ? and Private_key = ?",(Email,Private_key,))
        rows = cur.fetchall()
        for row in rows:
            print("Hi")
            PWD = row[7]
            print(PWD)
            email_reporting(Email, "Security Mail sent for password verification", PWD)
        #msg = Message('Password: ',sender = 'teamfashionera04@gmail.com', recipients = [Email])  
        #msg.body = 'Your password is: ' + str(PWD) 
        #mail.send(msg) 
    return render_template("forgot_page.html")#rendering html page

def email_reporting(to,subject,BodyText):    
    msg = MIMEMultipart() 
    msg['From']= EMAIL_ID
    msg['To']= to
    msg['Subject']= subject

    # add in the message body
    msg.attach(MIMEText(BodyText, 'html'))

    # html = ""
    # msg = MIMEText(html.read(), 'html')
   
    print(msg)
  
    # send the message via the server set up earlier.
    s.send_message(msg)

@app.route("/delete_page",methods=['GET','POST'])
def delete_page():
    database = r"C:\IBM Hack Challenge\database.db"
    conn = connection(database)
    if request.method=='POST':
        Email = request.form['Email']
        PWD = request.form['password']
        print(Email)
        print(PWD)
        sql = '''insert into Backup_Data(ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key) select ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key from User_Data where Email = ? and PWD=?'''
        cur = conn.cursor()
        cur.execute(sql,(Email,PWD,))
        conn.commit()
        id = deletemain(conn, Email, PWD)

    return render_template("delete_page.html")

def deletemain(conn, Email, PWD):
    sql = 'delete from User_Data where Email = ? and PWD=?'
    cur = conn.cursor()
    cur.execute(sql,(Email,PWD,))
    print("\nData deleted sucessfully")
    conn.commit()

def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print("Connection stablished successfully")
    except Error as e:
        print("Database opening error")
    return conn

@app.route("/signup_page",methods=['GET','POST'])
def signup_page():
    try:
        database = r"C:\IBM Hack Challenge\database.db"
        conn = connection(database)
        with conn:
            if request.method=='POST':
                a = [0,1,2,3,4,5,6,7,8,9]
                ID = id(a)
                print("Connected!!!")
                Name = request.form['Name']
                Email = request.form['Email']
                Address = request.form['Address']
                DOB = request.form['DOB']
                Mob_No = request.form['MobileNo']
                UserName = request.form['Username']
                PWD = request.form['password']
                Private_key = request.form['private key']
                print("Name: ", Name)
                print("Email ID: ", Email)
                print("Address: ", Address)
                print("D.O.B: ", DOB)
                print("Contact: ", Mob_No)
                print("Username: ", UserName)
                print("Password: ", PWD)
                print("Private Key: ", Private_key)
                sql = '''insert into User_Data(ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key) values(?,?,?,?,?,?,?,?,?)'''
                cur = conn.cursor()
                data = (ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key,)
                cur.execute(sql,data)
                conn.commit()
                rows=0
                cur.execute("Select * from User_Data where Name = ? and Email = ? and PWD = ?",(Name,Email,PWD,))
                rows = cur.fetchall()
                for row in rows:
                    print("\nYour System Generated Unique ID \n: ",row[0])
                flash("Account is created succesfully.")
                return redirect(url_for('signup_page'))
    except Error as e:
        print("Error in database connection",e)
    return render_template("signup_page.html")

global i
@app.route("/main_page",methods=["GET","POST"]) #route for our prediction
def upload():
    if request.method=='POST':
        print("inside main")
        f=request.files['image'] #requesting the file
        basepath=os.path.dirname('__file__')#storing the file directory
        filepath=os.path.join(basepath, f.filename)#storing the file in uploads folder
        f.save(filepath)#saving the file
        
        img=image.load_img(filepath,target_size=(64,64)) #load and reshaping the image
        x=image.img_to_array(img)#converting image to array
        x=np.expand_dims(x,axis=0)#changing the dimensions of the image
        
        pred=model.predict_classes(x)#predicting the results
        print("prediction",pred)#printing the prediction
        index =["Type-I", "Type-II", "Type-III"]
        print("index: " , index)
        	
        text = "The predicted color is: " + str(index[pred[0]])
        print("text:", text)

    if request.method == 'GET':
        return render_template("main_page.html")
    elif request.method == 'POST':
        payload = request.json
        print(payload)
        if i == 0:
            a = payload['Event']
            print("single: ", payload['Event'])
            i = 1
        elif i == 1:
            b = payload['Gender']
            print(payload['Gender'])
            print(b)
        return "Message Recieved"
    else:
        print("Else: ", request.data)
        return "200"
    return render_template("main_page.html")


#port = int(os.getenv("PORT"))
if __name__=="__main__":
    app.run(debug=True)#running our app
    #app.run(host='0.0.0.0', port=8000,debug=False)
            
            