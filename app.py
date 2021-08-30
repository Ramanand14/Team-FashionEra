import os
import numpy as np

#Flask - It is our framework which we are going to use to run/serve our application.
#request - used for accessing file which was uploaded by the user on our application.
#render_template - used for rendering the html pages
from flask import Flask,request,render_template,flash,redirect,url_for  

from werkzeug.utils import secure_filename

from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing import image

#Required libraries to use sqlite database
import sqlite3
from sqlite3 import Error

import smtplib

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# declare global variable outside the function
condition1 = 0
condition2 = 0
a = 0
b = 0
c = 0
d = 0
UserName = 0
PWD = 0
Email = 0

#our flask app
app=Flask(__name__, template_folder='template/HTML')

#loading the model
model=load_model(r'color_1.h5')

app.secret_key = "abc"  

# Email ID and password we are going to use to send an email
EMAIL_ID = "teamfashionera04@gmail.com"
PASSWORD = "FashionEra@1289"
SMTP_PORT = 587

s = smtplib.SMTP(host='smtp.gmail.com', port=SMTP_PORT)
s.starttls()
s.login(EMAIL_ID,PASSWORD)

#Define intro function which is the root page of our web application
@app.route("/",methods=['GET','POST']) #default route
def intro():
    #access global variables into the function
    global condition1
    global a, b, c, d
    if request.method == 'GET':
        return render_template("intro_page.html")

    #Revcieve chatbot responses using ngrok as a medium
    elif request.method == 'POST':
        payload = request.json
        if condition1 == 0:
            a = payload['Event']
            condition1 = 1
        elif condition1 == 1:
            b = payload['Gender']
            condition1 = 2
        elif condition1 == 2:
            c = payload['Age']
            condition1 = 3
        elif condition1 == 3:
            d = payload['Size']
            condition2 = 2
            return render_template("main_page.html")
        return "Message Recieved"

    else:
        return "200"
    return render_template("intro_page.html")#rendering html page

#Define about function which will open the about_page of our web application
@app.route("/about_page") 
def about():
	return render_template("about_page.html")#rendering html page

#Define help function which will open the help_page of our web application
@app.route("/help_page") 
def help():
	return render_template("help_page.html")#rendering html page

#Define help function which will open the camera_page of our web application
@app.route("/camera_page") 
def camera_page():
	return render_template("camera_page.html")#rendering html page

#Define login function which will open the login_page of our web application
@app.route("/login_page",methods=['GET','POST'])
def login():
    #access global variables into the function
    global UserName
    global PWD
    database = r"database.db"
    conn = connection(database)
    if request.method=='POST':
        #take username and password from the template
        UserName = request.form['username']
        PWD = request.form['password']
        rows=0
        cur = conn.cursor()
        cur.execute("Select * from User_Data where UserName = ? and PWD = ?",(UserName,PWD,))
        rows = cur.fetchall()
        for row in rows:
            #If there is no such match of username and password, reopen the login page and display the flash message
            if rows is None:
                flash("Invalid username or password.", category='error')
                return render_template("login_page.html")
            #If there exist such match of username and password, kindly open mainpage of web application
            else:
                return render_template("main_page.html")
	
    return render_template("login_page.html")

#Define forgot_page function which will open the forgot_page of our web application
@app.route("/forgot_page",methods=['GET','POST']) 
def forgot_page():
    #access global variables into the function
    global Email
    database = r"database.db"
    conn = connection(database)
    if request.method=='POST':
        #take username and password from the template
        Email = request.form['Email']
        Private_key = request.form['private_key']
        rows=0
        cur = conn.cursor()
        cur.execute("Select * from User_Data where Email = ? and Private_key = ?",(Email,Private_key,))
        rows = cur.fetchall()
        for row in rows:
            #If there is no such match of email id and private key, reopen the forgot page and display the flash message
            if rows is None:
                flash("Invalid Email or private key.", category='error')
                return render_template("forgot_page.html")
            #If there exist such match of email id and private key, kindly send the respective mail given below along with displaying flash message
            else:
                flash("Password has been sent to you. Kindly check your mailbox PRIMARY or SPAM.", category='success')
                e_msg = "Hi <b>"+ str(row[6]) +"</b>,<br><br><br>We have sent you this email in response to your request to forgot password.<br><br>Your password is <b>"+ str(row[7]) +"</b>.<br><br>We recommend that keep your password secure and not to share it with anyone.The respective mail is generated by the demo site of the Team FashionEra created for the IBM Hack Challenge - 2021.<br><br><br><br>Thank You,<br>Best Regards,<br>Team FashionEra"
                email_reporting(Email, "Request for the password check.", e_msg)
                return render_template("forgot_page.html")

    return render_template("forgot_page.html")#rendering html page

#Define email_reporting function which will send an email
def email_reporting(to,subject,BodyText):    
    msg = MIMEMultipart() 
    msg['From']= EMAIL_ID
    msg['To']= to
    msg['Subject']= subject

    # add in the message body
    msg.attach(MIMEText(BodyText, 'html'))
  
    # send the message via the server set up earlier.
    s.send_message(msg)

#Define delete_page function which will open the delete_page of our web application
@app.route("/delete_page",methods=['GET','POST'])
def delete_page():
    #access global variables into the function
    global Email
    global PWD
    database = r"database.db"
    conn = connection(database)
    if request.method=='POST':
        Email = request.form['Email']
        PWD = request.form['password']
        rows=0
        cur = conn.cursor()
        cur.execute("Select * from User_Data where Email = ? and PWD = ?",(Email,PWD,))
        rows = cur.fetchall()
        for row in rows:
            #If there is no such match of email id and password, reopen the delete page and display the flash message
            if rows is None:
                flash("Account with given Email and Password does not exists.", category='error')
                return render_template("delete_page.html")
            #If there is such match of email id and password, kindly send the respective mail given below along with displaying flash message
            else:
                flash("Your account deleted successfully.", category='success')
                e_msg = "Hi <b>"+ str(row[6]) +"</b>,<br><br><br>We have sent you this email in response to your request to delete my account.<br><br>We would like to tell you that your account on the FashionEra got deleted succesfully.The respective mail is generated by the demo site of the Team FashionEra created for the IBM Hack Challenge - 2021.<br><br><br><br>Thank You,<br>Best Regards,<br>Team FashionEra"
                email_reporting(Email, "Account deletion is successful", e_msg)
                #store the account into another table for backup
                sql = '''insert into Backup_Data(ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key,User_Img) select ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key,User_Img from User_Data where Email = ? and PWD=?'''
                cur = conn.cursor()
                cur.execute(sql,(Email,PWD,))
                conn.commit()
                id = deletemain(conn, Email, PWD)
                return render_template("delete_page.html")

    return render_template("delete_page.html")

#Define deletemain function which will delete the user account
def deletemain(conn, Email, PWD):
    sql = 'delete from User_Data where Email = ? and PWD=?'
    cur = conn.cursor()
    cur.execute(sql,(Email,PWD,))
    conn.commit()

#Define connection function which will connect to database 
def connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print("Database opening error")
    return conn

#Define convertToBinary function which convert the image into binary bits and store into the database
def convertToBinaryData(filename):
    # Convert digital data to binary format
    with open(filename, 'rb') as file:
        blobData = file.read()
    return blobData

#Define signup_page function which will open the signup_page of our web application
@app.route("/signup_page",methods=['GET','POST']) #route for our prediction
def signup_page():
    try:
        database = r"database.db"
        conn = connection(database)
        with conn:
            if request.method=='POST':
                a = [0,1,2,3,4,5,6,7,8,9]
                ID = id(a)
                Name = request.form['Name']
                Email = request.form['Email']
                Address = request.form['Address']
                DOB = request.form['DOB']
                Mob_No = request.form['MobileNo']
                UserName = request.form['Username']
                PWD = request.form['password']
                Private_key = request.form['private key']
                User_Img = convertToBinaryData("user_image.jpg")
                cur = conn.cursor()
                sql = '''insert into User_Data(ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key,User_Img) values(?,?,?,?,?,?,?,?,?,?)'''
                data = (ID,Name,Email,Address,DOB,Mob_No,UserName,PWD,Private_key,User_Img,)
                cur.execute(sql,data)
                conn.commit()
                rows=0
                cur.execute("Select * from User_Data where Name = ? and Email = ? and PWD = ?",(Name,Email,PWD,))
                rows = cur.fetchall()
                for row in rows:
                    e_msg = "Hi <b>"+ str(row[6]) +"</b>,<br><br><br>We have sent you this email to notify you that your account on FashionEra is created successfully.<br><br>System generated unique id is <b>"+ str(row[0]) +"</b>.<br><br>We recommend that keep your password, private key and id secure and not to share it with anyone.The respective mail is generated by the demo site of the Team FashionEra created for the IBM Hack Challenge - 2021.<br><br><br><br>Thank You,<br>Best Regards,<br>Team FashionEra"
                    email_reporting(Email, "Account is created succesfully.", e_msg)
                flash("Account is created succesfully. Kindly Check your mail to see the system generated unique ID.", category='success')
                return redirect(url_for('signup_page'))
    except Error as e:
        flash("The given Email or UserName already exist. Please Kindly change it.", category='error')
    return render_template("signup_page.html")

#Define main_page function which will open the main_page of our web application
@app.route("/main_page",methods=["GET","POST"]) #route for our prediction
def upload():
    #access global variables into the function
    global condition1
    global condition2
    global a, b, c, d
    if condition2 == 0:
        if request.method == 'GET':
            return render_template("intro_page.html")
        if request.method=='POST':
            f=request.files['image'] #requesting the file
            basepath=os.path.dirname('__file__')#storing the file directory
            filepath=os.path.join(basepath, f.filename)#storing the file in uploads folder
            f.save(filepath)#saving the file
            
            img=image.load_img(filepath,target_size=(64,64)) #load and reshaping the image
            x=image.img_to_array(img)#converting image to array
            x=np.expand_dims(x,axis=0)#changing the dimensions of the image
            
            pred=model.predict_classes(x)#predicting the results
            index =["Type-I", "Type-II", "Type-III"]
            print("index: " , index)

            text = "The predicted color is: " + str(index[pred[0]])
            skin = str(index[pred[0]])
            print(skin)

            #check the conditions to give fashion recommendation
            result1 = a
            result2 = b
            result3 = c
            result4 = d
            if result1 == 'Corporate Industry Outfits':
                return render_template("outfit1.html", gen = b, age = c, size = d, tone = skin)             
            elif result1 == 'Daily Outfits':
                return render_template("outfit2.html", gen = b, age = c, size = d, tone = skin)   
            elif result1 == 'Army Outfits':
                return render_template("outfit3.html", gen = b, age = c, size = d, tone = skin)
            elif result1 == 'Casual Outfits':
                return render_template("outfit4.html", gen = b, age = c, size = d, tone = skin)   
            elif result1 == 'Wedding Outfits':
                return render_template("outfit5.html", gen = b, age = c, size = d, tone = skin)   
            elif result1 == 'Accessories':
                return render_template("outfit6.html", gen = b, age = c, size = d, tone = skin)   
            elif result1 == 'Season Outfits':
                return render_template("outfit7.html", gen = b, age = c, size = d, tone = skin)   
            else:
                return render_template("outfit8.html", gen = b, age = c, size = d, tone = skin)

    return render_template("main_page.html")

#Define profile_page function which will open the profile_page of our web application
@app.route("/profile_page", methods=["GET","POST"]) 
def profile_page():
    #access global variables into the function
    global UserName
    global PWD
    
    database = r"database.db"
    conn = connection(database)
    rows=0
    cur = conn.cursor()
    cur.execute("Select * from User_Data where UserName = ? and PWD = ?",(UserName,PWD,))
    rows = cur.fetchall()
    for row in rows:
        photo = row[9]
        photoPath = "C:\IBM Hack Challenge\static\Images\\" + UserName + ".jpg"
        writeTofile(photo, photoPath)
        return render_template("profile_page.html", user = UserName, pwd = PWD, email = row[2], phn = row[5], name = row[1], dob = row[4], addrs = row[3], img = UserName)

    return render_template("profile_page.html")#rendering html page

#Define writeTofile function which will convert the binary image from the dataset
def writeTofile(data, filename):
    # Convert binary data to proper format and write it on Hard Disk
    with open(filename, 'wb') as file:
        file.write(data)
    print("Stored blob data into: ", filename, "\n")

#Define update_page function which will open the update_page of our web application
@app.route("/update_page",methods=['GET','POST'])
def update_page():
    #access global variables into the function
    global Email
    try:
        database = r"database.db"
        conn = connection(database)
        with conn:
            if request.method=='POST':
                username = UserName
                password = PWD
                Name = request.form['Name']
                Address = request.form['Address']
                DOB = request.form['DOB']
                Mob_No = request.form['MobileNo']
                Private_key = request.form['private key']
                User_Img = convertToBinaryData("user_image.jpg")
                cur = conn.cursor()
                data = (Name,Address,DOB,Mob_No,Private_key,username,password)
                sql = '''update User_Data set Name = ?, Address = ?, DOB = ?, Mob_No = ?, Private_key = ? where UserName = ? and PWD = ? '''
                cur = conn.cursor()
                cur.execute(sql,data)
                conn.commit()
                
                e_msg = "Hi <b>"+ username +"</b>,<br><br><br>We have sent you this email to notify you that your account details on FashionEra are updared successfully.<br><br>We recommend that keep your password, private key and id secure and not to share it with anyone.The respective mail is generated by the demo site of the Team FashionEra created for the IBM Hack Challenge - 2021.<br><br><br><br>Thank You,<br>Best Regards,<br>Team FashionEra"
                email_reporting(Email, "Account detials are updated succesfully.", e_msg)
                flash("Account details are updated succesfully. Kindly Check your mail to see the the confirmation email.", category='success')
                return redirect(url_for('update_page'))
    except Error as e:
        flash("The given Email or UserName already exist. Please Kindly change it.", category='error')

    return render_template("update_page.html")

#port = int(os.getenv("PORT"))
if __name__=="__main__":
    app.run(debug=True)#running our app
            