import os
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from dotenv import load_dotenv

load_dotenv()


class SendMail:

    def __init__(self):
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.sender_password = os.getenv("SENDER_PASSWORD")
        self.session = smtplib.SMTP('smtp.gmail.com', 587)  # use the Gmail SMTP server
        self.session.starttls()  # enable security
        self.session.login(self.sender_email, self.sender_password)  # login with Gmail account

    def send_email(self, receiver_email, subject, body):
        # Set up the MIME
        message = MIMEMultipart()
        message['From'] = sender_email
        message['To'] = receiver_email
        message['Subject'] = subject

        # Add body to email
        message.attach(MIMEText(body, 'plain'))

        # Send the email
        text = message.as_string()
        self.session.sendmail(self.sender_email, receiver_email, text)
        self.session.quit()
        print('Mail Sent')
        return True

# Example usage
sender_email = 'your_email@gmail.com'  # Your Gmail address
sender_password = 'your_password'  # Your Gmail password
receiver_email = 'recipient_email@example.com'  # Recipient's email address
subject = 'Test Email'
body = 'Hello, this is a test email from Python!'


