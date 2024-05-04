from sendmail import SendMail

send = SendMail()


def password_reset(email):
    body = "reset your password here!!!"
    subject = "Password Reset"
    SendMail.send_email(email, subject, body)
    return True
