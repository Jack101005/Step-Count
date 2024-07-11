from datetime import datetime
from flask import render_template
from CALORIE-APP-MAIN import app
from datetime import datetime
from flask import render_template, request, redirect, url_for, jsonify, flash
from flask import Flask, render_template, request
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length

import csv
import secrets

app.config["SECRET_KEY"] = "Th1sKrC@re"
app.config['DEBUG'] = True
app.config["SECRET_KEY"] = secrets.token_urlsafe(16)


@app.route('/checkLogin', methods=['POST','GET'])
def checkLogin():
    if request.method == 'POST':
        email = request.form['first']
        password = request.form['password']
        user_found = False
        with open('user_database.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:
                    user_found = True
                    hashed_password = row[1]
                    if hashed_password == password:
                        return redirect(url_for("dashboard"))  # Redirect to dashboard
                    else:
                        error_message = "Incorrect password. Please try again."
                        return render_template('loginpassworderror.html', title='Start to Login', year=datetime.now().year, message='Your login page. ', error=error_message)
        if not user_found:
            error_message = "This email is not sign up yet. Please sign up."
            return render_template('loginemailerror.html', title='Start to Sign up', year=datetime.now().year, message='Your sign up page. ', error=error_message)
    else:
        return redirect(url_for("checkLogin"))
   


@app.route('/register', methods=["GET", "POST"])
def register():
    if request.method == "POST":
        email = request.form["email"]
        password = request.form["password1"]
        # Validation: Check if all fields are filled
        if not email or not password:
            return render_template(
                'createaccounterror.html',
                title='User Main Page',
                year=datetime.now().year,
                message='Please fill in all the required fields.'
            )
        with open('user_database.csv', 'r') as file:
            reader = csv.reader(file)
            for row in reader:
                if row[0] == email:
                    error_message = "This email has already signed up. Please sign up with another email."
                    return render_template('alreadyemail.html', title='Start to Sign up', year=datetime.now().year, message='Your sign up page. ', error=error_message)
                
        with open('user_database.csv', 'a', newline='') as file:
            writer = csv.writer(file)
            writer.writerow([email, password])
            #save_user_data(email, password)
            return redirect(url_for("success"))
    else:
        return redirect(url_for("createaccount"))