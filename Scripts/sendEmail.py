import os
import sys
import ssl
from email.message import EmailMessage
import smtplib

sender = "taylorldelbridge@gmail.com"
password = "jjkzxjgpztsgqhzy"
reciever = sys.argv[1]
subject = sys.argv[2]
body = sys.argv[3]

em = EmailMessage()
em['From'] = sender
em['To'] = reciever
em['Subject'] = subject
em.set_content(body)

context = ssl.create_default_context()

with smtplib.SMTP_SSL('smtp.gmail.com',465, context=context) as smtp:
    smtp.login(sender, password)
    smtp.sendmail(sender, reciever, em.as_string())