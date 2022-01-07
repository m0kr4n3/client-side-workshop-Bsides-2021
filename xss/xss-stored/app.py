#!/usr/bin/python3
from flask import Flask, Response, redirect, request, jsonify, render_template, make_response
import base64 as b64
import json

app = Flask(__name__)

users = {"admin":"jslkdfjlkjxo8"}
notes = []
vuln = "<span>{message}<br/></span><br/><hr/>"

@app.route("/", methods=["GET", "POST"])
def root():
    cookie = request.cookies.get('session')
    if cookie == None :
        return redirect("login")
    return redirect("home") 


@app.route("/login",methods=["GET","POST"])
def login():
    cookie = request.cookies.get('session')
    if cookie == None :
        redirect('/')
    if request.method == "POST":
        data = request.form
        if data['Username'] in users :
            if data['Password'] == users[data['Username']]:
                    dic = {'Username':data['Username'],'Password':data['Password']}
                    session = b64.b64encode(json.dumps(dic).encode()).decode()
                    resp = make_response(redirect('/'))
                    resp.set_cookie('session',session)
                    return resp
            else :
                return render_template('login.html',error=True,content="Wrong password")
        else :
            if data['Username'] != '' and data['Password'] != '' :
                users[data['Username']] = data['Password']
                return render_template('login.html',sucess=True)
            return render_template('login.html',error=True,content="Username and password can't be empty")

    return render_template('login.html')

@app.route("/home",methods=["GET","POST"])
def home():
    cookie = request.cookies.get('session')
    if cookie == None :
        return redirect('/')
    data = json.loads(b64.b64decode(cookie))
    if "Username" in data and data['Username'] in users and "Password" in data  and users[data["Username"]] == data["Password"]   :
        if request.method == "POST" :
            mssg = request.form.get("message")
            if mssg :
                notes.append(mssg)
        mssgs = ""
        for note in notes : 
            mssgs+= vuln.format(message=note)
        
        with open("bad.html") as f :
            return f.read().format(user=data["Username"],mssgs=mssgs)


    return redirect('/login')