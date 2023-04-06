from os import environ as environment
from email.message import EmailMessage
import ssl
import smtplib


class EmailSender:
    def __init__(self):
        self.email_password = environment.get('email_password', 'error')
        self.email_address = environment.get('email_address', 'error')
        if self.email_address == 'error' or self.email_password == 'error':
            print('Environment variables are not set')

    def send_forgot_password_email(self, receiver, forgot_password_link):
        subject = 'jBay: Forgot Password'
        body = \
            f"""If you've lost your password or wish to reset it, please use the link below.
            {forgot_password_link}
            If you did not request a password reset please ignore this email.
            """
        em = EmailMessage()
        em['From'] = self.email_address
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.sendmail(self.email_address, receiver, em.as_string())

    def send_confirmation_email(self, receiver, link):
        subject = 'jBay: Confirm Your Email'
        body = f"Click here to confirm your email:{link}"
        em = EmailMessage()
        em['From'] = self.email_address
        em['To'] = receiver
        em['Subject'] = subject
        em.set_content(body)
        context = ssl.create_default_context()
        with smtplib.SMTP_SSL('smtp.gmail.com', 465, context=context) as smtp:
            smtp.login(self.email_address, self.email_password)
            smtp.sendmail(self.email_address, receiver, em.as_string())
