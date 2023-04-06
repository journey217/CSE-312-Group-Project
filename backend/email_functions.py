import os
from email.message import EmailMessage
import ssl
import smtplib


def forgot_password_email(receiver, forgot_password_link):
    email_sender = 'ubcodingprojects@gmail.com'
    email_password = ''  # Need to add using env variable and docker

    subject = 'jBay: Forgot Password'
    body = f"""If you've lost your password or wish to reset it, please use the link below.
            {forgot_password_link}
            
            If you did not request a password reset please ignore this email."""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, receiver, em.as_string())


def send_confirmation_email(receiver, link):
    email_sender = 'ubcodingprojects@gmail.com'  # Junk email password is CSE312!!
    email_password = 'utgnarugxwpegyne'  # Need to remove using env variable and docker
    email_receiver = receiver  # Should be actual email address receiver

    subject = 'jBay: Confirm Your Email'
    body = f"""Click here to confirm your email:
            {link}"""

    em = EmailMessage()
    em['From'] = email_sender
    em['To'] = email_receiver
    em['Subject'] = subject
    em.set_content(body)
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
        smtp.login(email_sender, email_password)
        smtp.sendmail(email_sender, email_receiver, em.as_string())
