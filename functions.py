import numpy as np
from config import mail
from flask_mail import Message

def genString(length):
    alphabet = list('abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789')
    np_alphabet = np.array(alphabet, dtype="|S1")
    np_codes = np.random.choice(np_alphabet, length)
    codes = "".join(np_codes)
    return codes

def send_email(email, subject, html):
    msg = Message(
           subject,
           sender = email,
           recipients = [email])
    msg.body = html
    mail.send(msg)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS
