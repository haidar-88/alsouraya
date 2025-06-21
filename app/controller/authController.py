from flask import Blueprint, render_template, request, session, redirect
from app.service import authService

auth_bp = Blueprint('auth', __name__)

@auth_bp.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    else:
        data = request.get_json()

        if authService.find_admin(data):
            session.permanent = False
            session['username'] = data.get("username")
            session['password'] = data.get("password")
            session['role'] = 'admin'
            return redirect('/admin-page')
        
        response = authService.find(data)
        if response:
            session.permanent = False
            session['username'] = data.get("username")
            session['password'] = data.get("password")
            session['role'] = 'user'
            return "Ok", 200
    return 'Error cannot find account', 400

@auth_bp.route("/signup", methods=['GET', 'POST'])
def signup(): 
    if request.method == 'GET':
        return render_template('signup.html')
    else:
        data = request.get_json()
        response = authService.addUser(data)
        if (response):
            session.permanent = False
            session['username'] = data.get("username")
            session['password'] = data.get("password")
            session['role'] = 'user'
            return 'Ok', 200
        return 'Username Taken', 400