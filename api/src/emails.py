from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib

def send_magic_link(email, token, settings):
    # Create the email message
    msg = MIMEMultipart()
    msg['From'] = settings.admin_email
    msg['To'] = email
    msg['Subject'] = "Login to YourApp"
    body = "Click the following link to log in: " + settings.server_url + f"/api/verify?user_token={token}&email={email}"
    msg.attach(MIMEText(body, 'plain'))

    # Connect to the email server and send the email
    with smtplib.SMTP("smtp.office365.com", 587) as server:
        server.starttls()
        server.login(settings.admin_email, settings.admin_password)       
        server.send_message(msg)