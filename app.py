import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask,redirect,url_for,render_template,request, jsonify
import requests
from pymongo import MongoClient
from datetime import datetime

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URL")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient(MONGODB_URI)
db = client[DB_NAME]

app=Flask(__name__)
@app.route('/',methods=['GET'])
def home():
    return render_template('index.html')

@app.route('/diary', methods=['GET'])
def show_diary():
    # sample_receive = request.args.get('sample_give')
    # print(sample_receive)
    # return jsonify({
    #     'msg':'data telah diterima'
    # })
    articles = list(db.diary.find({},{'_id':False}))
    return jsonify({'articles': articles})


@app.route('/diary', methods=['POST'])
def save_diary():
    # sample_receive = request.form['sample_give']
    # print(sample_receive)
    # return jsonify({'msg': 'POST request complete!'})
    title_receive = request.form["title_give"]
    content_receive = request.form["content_give"]

    today = datetime.now()
    date_time = today.strftime('%Y-%m-%d-%H-%M-%S')
    
    file = request.files['files_give']
    extention = file.filename.split('.')[-1]
    today = datetime.now()
    date_time = today.strftime('%Y-%m-%d-%H-%M-%S')
    filename = f'static/post-{date_time}.{extention}'
    file.save(filename)
    
    profile = request.files['profile_give']
    extention = profile.filename.split('.')[-1]
    today = datetime.now()
    date_time = today.strftime('%Y-%m-%d-%H-%M-%S')
    fileprofile = f'static/profile-{date_time}.{extention}'
    profile.save(fileprofile)

    waktu = today.strftime('%Y-%m-%d')

    doc = {
        'profile': fileprofile,
        'file': filename,
        'title': title_receive,
        'content': content_receive,
        'time': waktu
    }
    db.diary.insert_one(doc)

    return jsonify({'msg':'Upload complete!'})

if __name__ == '__main__':
    #DEBUG is SET to TRUE. CHANGE FOR PROD
    app.run('0.0.0.0',port=5000,debug=True)