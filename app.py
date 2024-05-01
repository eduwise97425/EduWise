from flask import Flask, request, redirect, url_for, render_template, flash
import os
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import random

app = Flask(__name__)  # Instance of Flask
current_dir = os.path.abspath(os.path.dirname(__file__))  # Gets the absolute path of the directory where the current Python script resides
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///" + os.path.join(current_dir, "database.sqlite3")  # Configures the SQLAlchemy database URI for our Flask application to use a SQLite database located in the same directory as the current script
db = SQLAlchemy(app)  # Creates an instance of the SQLAlchemy class and binds it to our Flask application (app)


# Creating database models
class User(db.Model):
    Username = db.Column(db.String, primary_key=True)
    Password = db.Column(db.String, nullable=False)
    Email = db.Column(db.String, nullable=False, unique=True)


# creating route for login_error
@app.route('/login_error', methods=['GET'])
def login_error():
    if request.method == 'GET':
        return render_template('login_error.html')


# creating route for landing page
@app.route('/', methods=['GET'])
def landingpage():
    if request.method == 'GET':
        return render_template("eduwise.html")


# creating route for login page
@app.route('/login', methods=['GET','POST'])
def loginpage():
    if request.method == 'GET':
        return render_template('login.html')
    elif request.method == 'POST':
        a = request.form.get('Username')
        b = request.form.get('Password')
        y = User.query.all()
        l = []
        for i in y:
            l.append((i.Username, i.Password))
        if (a, b) in l:
            data = a
            return redirect(url_for('dashboard', data=data))
        else:
            return redirect('/login_error')


# creating route for signup page
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'GET':
        return render_template('signup.html')
    elif request.method == 'POST':
        a = request.form.get('Username')
        b = request.form.get('Password')
        c = request.form.get('Email')
        data = User(Username=a, Password=b, Email=c)
        l = []
        users_list = User.query.all()
        for i in users_list:
            l.append((i.Username, i.Password, i.Email))
        if (a, b, c) not in l:
            db.session.add(data)
            db.session.commit()
            return redirect('/login')
        else:
            return redirect('/already_account_exists')

# creating route for already_account_exists page
@app.route('/already_account_exists', methods=['GET'])
def existing_user():
    if request.method == "GET":
        return render_template('already_account_exists.html')

# creating route for input page
@app.route('/Input_Page', methods=['GET','POST'])
def inputpage():
    if request.method == 'GET':
        return render_template("Input_Page.html")
    elif request.method == 'POST':
        a = request.form.get('')
# Creating Routes for Dashboard Section Dedicated!

@app.route('/Dashboard_Page', methods=['GET'])
def dashboard():
    if request.method == 'GET':
        data = request.args.get('data')
        return render_template('Dashboard_Page.html', user=data)

@app.route('/Blog_Page', methods=['GET'])
def Blog_Page():
    if request.method == 'GET':
        return render_template('Blog_Page.html')

@app.route('/generated_output',methods = ['GET'])
def Generate_output():
    if request.method == 'GET':
        return render_template('generate_schedule.html')

@app.route('/Generate_Page', methods=['GET'])
def Generate_Page():
    if request.method == 'GET':
        return render_template('Generate_Page.html')

@app.route('/Note_Pad', methods=['GET'])
def Note_Pad():
    if request.method == 'GET':
        return render_template('Note_Pad.html')

@app.route('/Team_Page', methods=['GET'])
def Team_Page():
    if request.method == 'GET':
        return render_template('Team_Page.html')

def generate_schedule(total_days, subjects, start_date):
    time_array = ["8:00 AM - 10:00 AM", "10:30 AM - 12:30 PM", "1:00 PM - 2:00 PM", "3:00 PM - 4:30 PM", "6:00 PM - 7:00 PM", "7:30 PM - 9:00 PM"]
    
    # Convert start_date to datetime object
    start_date = pd.to_datetime(start_date)
    
    # Generate date ranges
    date_range = [start_date + pd.Timedelta(days=i) for i in range(total_days)]

    # Create an empty DataFrame to store the schedule
    schedule = pd.DataFrame(index=time_array, columns=date_range)

    # Fill the schedule with placeholders
    for date in date_range:
        for time_slot in time_array:
            schedule.loc[time_slot, date] = random.choice(subjects)

    return schedule

@app.route('/', methods=["GET", "POST"])
def input_form():
    if request.method == "POST":
        total_days = int(request.form['number'])  # Total number of days
        start_date = request.form['date']  # Start date
        subjects = request.form.getlist('subject')  # Selected subjects

        # Generating schedule using user input
        schedule = generate_schedule(total_days, subjects, start_date)
        schedule_html = schedule.to_html(classes='table table-striped', header=True, index=True, na_rep='')

        # Pass schedule and other necessary data to the template
        return render_template("generate_schedule.html", schedule_html=schedule_html, total_days=total_days, start_date=start_date, subjects=subjects)
    
    return render_template("Input_Page.html")

if __name__ == "__main__":
    app.run(debug=True, port=8080)