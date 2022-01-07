#!/usr/bin/python3
from flask import Flask, Response, redirect, request, jsonify, render_template, make_response
import json


app = Flask(__name__)


@app.route("/", methods=["GET","POST"])
def root():
    title, mssg = request.args.get("title"), request.args.get("message")
    if title and mssg : 
        with open("bad.html") as f :
            return f.read().format(title=title,message=mssg)
    return render_template('tst.html')  
    return "Only GET/POST methods are supported"
