from flask import render_template,redirect,flash,url_for,request
from .import home

@home.route('/')
def index():
    return render_template('home/index.html')

@home.route('/')
def login():
    return render_template('home/login.html')