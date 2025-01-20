from flask import Flask, request, jsonify
from flask_cors import CORS
import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
CORS(app, resources={r"/api": {"origins": "*"}})


@app.route("/api", methods=["POST"])
def contact():
    data = request.json
    name = data['firstName'] + data['lastName']
    email = data['email']
    message = data['message']
    phone = data['phone']
    
    mail = MIMEMultipart()
    mail['From'] = os.getenv('EMAIL_USER')
    mail['To'] = "website@sgalek.com"
    mail['Subject'] = "Contact Form Submission - Portfolio"
    
    html = f"<p>Name: {name}</p><p>Email: {email}</p><p>Phone: {phone}</p><p>Message: {message}</p>"
    mail.attach(MIMEText(html, 'html'))
    
    try:
        with smtplib.SMTP_SSL("smtppro.zoho.eu", 465) as server:
            server.login(os.getenv('EMAIL_USER'), os.getenv('EMAIL_PASS'))
            server.send_message(mail)
        return jsonify({"code": 200, "status": "Message Sent"})
    except Exception as e:
        print(jsonify(str(e)))
        return jsonify(str(e))

if __name__ == "__main__":
    app.run(port=5000)
    print("Server Running")

