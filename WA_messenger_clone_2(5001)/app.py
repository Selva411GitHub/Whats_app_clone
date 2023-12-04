from flask import Flask,render_template,request,url_for,redirect

app = Flask(__name__)
import json
import requests
import pymongo
from pymongo import MongoClient

client = pymongo.MongoClient("mongodb://localhost:27017/wa_clone")
db = client["wauser"]
collection = db["selva"]
data_col = collection.find()

@app.route('/read')
def home():
    data= collection.find()
    return render_template("home.html",data=data)

@app.route('/del/<id>')
def delete(id):
    id = int(id)-1
    id_data= collection.find()[id]
    collection.delete_one(id_data)
    return redirect(url_for('messaging'))


@app.route('/edit/<id>',methods=['POST','GET'])
def edit(id):
    id = int(id)-1
    id_data= collection.find()[id]
    if request.method=="POST":
        get_dic={}
        get_dic['name']=id_data['name']
        get_dic['msg']=request.form['msg']
        collection.update_one(id_data,{"$set":get_dic})  
        return redirect(url_for('messaging'))
    return render_template('text.html',id_data=id_data,data_col=data_col)

@app.route('/api',methods=['POST','GET'])
def api():
     if request.method=="POST":
        data=request.json
        collection.insert_one(data)  
        return redirect(url_for('messaging'))
     return redirect(url_for('messaging')) 

@app.route('/',methods=['POST','GET'])
def messaging():
    if request.method == 'POST':
        msg = request.form['msg']
        sms = {}
        sms.update({'name':'selva'})
        sms.update({"msg":msg})
        url="http://127.0.0.1:5000/api"
        response=requests.post(url,json=sms)
        return redirect(url_for('messaging'))
    data = collection.find()
    return render_template('home.html',data =data)


if __name__ == "__main__":
    app.run(debug=True,port=5001)