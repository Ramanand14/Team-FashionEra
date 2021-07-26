import os
import numpy as np #used for numerical analysis
from flask import Flask,request,render_template# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
#render_template- used for rendering the html pages
from tensorflow.keras.models import load_model#to load our trained model
from tensorflow.keras.preprocessing import image
import sqlite3
from sqlite3 import Error

app=Flask(__name__, template_folder='template/HTML')#our flask app
model=load_model(r'color_1.h5')#loading the model

@app.route("/") #default route
def about():
	return render_template("intro_page.html")#rendering html page

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
        if rows is None:
            return render_template("login_page.html")
        else:
            return render_template("main_page.html")
	
    return render_template("login_page.html")


@app.route("/delete_page",methods=['GET','POST'])
def delete_page():
    database = r"C:\IBM Hack Challenge\database.db"
    conn = connection(database)
    if request.method=='POST':
        Email = request.form['email']
        PWD = request.form['password']
        print(Email)
        print(PWD)
        sql = '''insert into Backup_Data(ID, USerName, Email, Cell, NickName, PWD) select ID,UserName,Email,Cell,NickName,PWD from User_Data where Email = ? and PWD=?'''
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
    #print("outside if")
    #print("Inside if")
    try:
        database = r"C:\IBM Hack Challenge\database.db"
        conn = connection(database)
        with conn:
            print("outside")
            if request.method=='POST':
                print("inside")
                a = [0,1,2,3,4,5,6,7,8,9]
                ID = id(a)
                print("Connected!!!")
                UserName = request.form['username']
                Email = request.form['email']
                Cell = request.form['mobile']
                NickName = request.form['user']
                PWD = request.form['pwd']
                print("Name: ", UserName)
                print("Email ID: ", Email)
                print("Contact: ", Cell)
                print("Nickname: ", NickName)
                print("Password: ", PWD)
                sql = '''insert into User_Data(ID,UserName,Email,Cell,NickName,PWD) values(?,?,?,?,?,?)'''
                cur = conn.cursor()
                data = (ID,UserName,Email,Cell,NickName,PWD)
                cur.execute(sql,data)
                conn.commit()
                rows=0
                cur.execute("Select * from User_Data where UserName = ? and Email = ? and PWD = ?",(ID,UserName,Email,Cell,NickName,PWD,))
                rows = cur.fetchall()
                for row in rows:
                    print("\nYour System Generated Unique ID \n: ",row[0])
    except Error as e:
        print("Error in database connection",e)
    return render_template("signup_page.html")

@app.route("/main_page",methods=["GET","POST"]) #route for our prediction
def upload():
    if request.method=='POST':
        #print("inside main")
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

    return render_template('/main_page.html')


#port = int(os.getenv("PORT"))
if __name__=="__main__":
    app.run(debug=True)#running our app
    #app.run(host='0.0.0.0', port=8000,debug=False)
            
            