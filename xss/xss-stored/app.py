#!/usr/bin/python3
from flask import Flask, redirect, request, render_template, make_response
import base64 as b64
import json

app = Flask(__name__)

users = {"admin@gmail.com":"superSecret"}
notes = []
vuln = "<span>{message}<br/></span><br/><hr/>"

@app.route("/", methods=["GET", "POST"])
def root():
    cookie = request.cookies.get('session')
    if cookie == None :
        return redirect("login")
    return redirect("home") 

@app.route("/home",methods=["GET","POST"])
def home():
    cookie = request.cookies.get('session')
    if cookie == None :
        return redirect('/')
    data = json.loads(b64.b64decode(cookie))
    if "Email" in data and data['Email'] in users and "Password" in data  and users[data["Email"]] == data["Password"]   :
        if request.method == "POST" :
            mssg = request.form.get("message")
            if mssg :
                notes.append(mssg)
        mssgs = ""
        for note in notes : 
            mssgs+= vuln.format(message=note)
        
        with open("home.html") as f :
            return f.read().format(email=data["Email"],mssgs=mssgs)
    else:
        return redirect('/login')

@app.route("/login",methods=["GET","POST"])
def login():
    cookie = request.cookies.get('session')
    if cookie == None :
        redirect('/')
    if request.method == "POST":
        data = request.form
        if data['Email'] in users :
            if data['Password'] == users[data['Email']]:
                    dic = {'Email':data['Email'],'Password':data['Password']}
                    session_cookie = b64.b64encode(json.dumps(dic).encode()).decode()
                    resp = make_response(redirect('/'))
                    
                    # Setting the cookie
                    resp.set_cookie('session',session_cookie)
                    
                    return resp
            else :
                return render_template('login.html',error=True,content="Wrong password")
        else :
            if data['Email'] != '' and data['Password'] != '' :
                users[data['Email']] = data['Password']
                return render_template('login.html',sucess=True)
            return render_template('login.html',error=True,content="Email and password can't be empty")

    return render_template('login.html')

@app.route("/changeEmail",methods=["GET","POST"])
def changeEmail():
    cookie = request.cookies.get('session')
    if cookie == None :
        return redirect('/')
    creds = json.loads(b64.b64decode(cookie))
    if "Email" in creds and creds['Email'] in users and "Password" in creds  and users[creds["Email"]] == creds["Password"]   :   
        if request.method == 'GET' :
            return render_template('changeEmail.html')
        elif request.method == "POST":
            data = request.form
            if data['newEmail'] in users :
                return render_template('changeEmail.html',error=True,content="Email already exists")
            else:
                password = creds["Password"]
                del users[creds["Email"]]
                users[data["newEmail"]] = password
                creds["Email"] = data["newEmail"]
                session_cookie = b64.b64encode(json.dumps(creds).encode()).decode()
                resp = make_response(redirect('/'))
                    
                # Setting the cookie
                resp.set_cookie('session',session_cookie)
                return resp

    else:
        return redirect('/')
    
    