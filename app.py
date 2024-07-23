from flask import Flask, render_template, request, redirect, url_for
import os
from datetime import datetime
from twilio.rest import Client
from dotenv import load_dotenv

app = Flask(__name__)

# Load environment variables from .env file
load_dotenv()

# Retrieve environment variables
TWILIO_ACCOUNT_SID = os.getenv('TWILIO_ACCOUNT_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')
TWILIO_PHONE_NUMBER = os.getenv('TWILIO_PHONE_NUMBER')
YOUR_PHONE_NUMBER = os.getenv('YOUR_PHONE_NUMBER')

# Initialize Twilio client
client = Client(TWILIO_ACCOUNT_SID, TWILIO_AUTH_TOKEN)

# Dummy storage for user credentials (Replace this with a database)
users = {}

# Dummy storage for print orders (Replace this with a database)
orders = []

# Ensure the uploads directory exists
UPLOAD_FOLDER = 'uploads'
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Configure the upload folder for Flask
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Route for registration
@app.route('/sign_up', methods=['GET', 'POST'])
def sign_up():
    if request.method == 'POST':
        number = request.form['number']
        user_name = request.form['uname']
        password = request.form['psw']
        password_repeat = request.form['psw-repeat']

        if password != password_repeat:
            return "Passwords do not match. Please try again."  
        
        if number in users:
            return "Mobile number already exists. Please choose another."

        users[number] = password
        return redirect(url_for('login'))

    return render_template('sign_up.html')

# Route for login
@app.route('/sign_in', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        number = request.form['number']
        password = request.form['psw']

        if number in users and users[number] == password:
            return redirect(url_for('choose'))
        else:
            return "Invalid username or password. Please try again."
    return render_template('sign_in.html')

# Route for choose.html (redirect target)
@app.route('/choose')
def choose():
    return render_template('choose.html')

# Route for print.html (form page)
@app.route('/print', methods=['GET', 'POST'])
def print_page():
    if request.method == 'POST':
        name = request.form['name']
        phone_number = request.form['phone_number']
        copies = request.form['copies']
        location = request.form['location']
        date = request.form['date']
        pdf_upload = request.files['pdf_upload']
        sides = request.form['sides']
        color = request.form['color']

        # Save the data (you should save this to a database in a real application)
        order = {
            'name': name,
            'phone_number': phone_number,
            'copies': copies,
            'location': location,
            'date': date,
            'pdf_upload': pdf_upload.filename,
            'sides': sides,
            'color': color
        }
        orders.append(order)

        # Save the uploaded file
        pdf_upload.save(os.path.join(app.config['UPLOAD_FOLDER'], pdf_upload.filename))

        return redirect(url_for('payment'))

    return render_template('print.html')

# Route for payment.html
@app.route('/payment')
def payment():
    return render_template('payment.html')

# Add routes for the individual payment options if needed
@app.route('/phonepe')
def phonepe():
    return render_template('phonepe.html')

@app.route('/card', methods=['GET', 'POST'])
def card():
    current_year = datetime.now().year
    if request.method == 'POST':
        # Process payment here
        message = client.messages.create(
            body="Your payment was successful!",
            from_=TWILIO_PHONE_NUMBER,
            to=YOUR_PHONE_NUMBER
        )
        return "Payment successful! Notification sent."
    return render_template('card.html', current_year=current_year)

@app.route('/cod')
def cod():
    return render_template('cod.html')

if __name__ == '__main__':
    app.run(debug=True)