from flask import Flask, request, render_template_string
import smtplib
from email.mime.text import MIMEText
import os
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

GMAIL_USER = os.getenv("GMAIL_USER")
GMAIL_PASS = os.getenv("GMAIL_PASS")
RECIPIENT = os.getenv("RECIPIENT")

@app.route('/')
def index():
    return render_template_string(open('email_notification_site.html', encoding='utf-8').read())

@app.route('/send-email', methods=['POST'])
def send_email():
    name = request.form['name']
    message = request.form['message']

    full_message = f"Tên: {name}\n\nLưu bút:\n{message}"
    msg = MIMEText(full_message)
    msg['Subject'] = 'Lưu bút điện tử của Huy Trần'
    msg['From'] = GMAIL_USER
    msg['To'] = RECIPIENT

    try:
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(GMAIL_USER, GMAIL_PASS)
            smtp.send_message(msg)
        return '✅ Email đã được gửi thành công!'
    except Exception as e:
        return f'❌ Gửi thất bại: {e}'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)