import os
import numpy as np #used for numerical analysis
from flask import Flask,request,render_template# Flask-It is our framework which we are going to use to run/serve our application.
#request-for accessing file which was uploaded by the user on our application.
#render_template- used for rendering the html pages
from tensorflow.keras.models import load_model#to load our trained model
from tensorflow.keras.preprocessing import image

app=Flask(__name__, template_folder='template/HTML')#our flask app
model=load_model(r'color_1.h5')#loading the model

@app.route("/") #default route
def about():
	return render_template("Intro_page.html")#rendering html page

@app.route("/Login_page.html")
def login():
	return render_template("Login_page.html")

@app.route("/Signup_page.html",methods=["GET","POST"])
def sign():
    print("outside if")
    if request.method=='POST':
        print("Inside if")
        n = request.form.get['username']
        print("Name: ", n)
    return render_template("Signup_page.html")









@app.route("/Main_page.html",methods=["GET","POST"]) #route for our prediction
def upload():
    payload = request.json
    print(payload)
    if request.method=='POST':
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

    return render_template('/Main_page.html')

#port = int(os.getenv("PORT"))
if __name__=="__main__":
    app.run(debug=True)#running our app
    #app.run(host='0.0.0.0', port=8000,debug=False)
            
            