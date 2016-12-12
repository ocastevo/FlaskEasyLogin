############################################################################
#this is SQLAlchemy architecture for the MYSQL database table of sharp.users
###########################################################################
from config import app
from db import db

# +-----------------+--------------+------+-----+---------+----------------+
# | Field           | Type         | Null | Key | Default | Extra          |
# +-----------------+--------------+------+-----+---------+----------------+
# | id              | int(11)      | NO   | PRI | NULL    | auto_increment |
# | username        | varchar(40)  | NO   |     | NULL    |                |
# | email           | varchar(50)  | NO   |     | NULL    |                |
# | first_name      | varchar(30)  | NO   |     | NULL    |                |
# | last_name       | varchar(30)  | NO   |     | NULL    |                |
# | password        | varchar(63)  | NO   |     | NULL    |                |
# | user_code       | varchar(30)  | NO   |     | NULL    |                |
# | profile_img     | varchar(100) | NO   |     | NULL    |                |
# | email_confirmed | tinyint(1)   | NO   |     | 0       |                |
# +-----------------+--------------+------+-----+---------+----------------+

class Users(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key = True)
    username = db.Column('username', db.String)
    email = db.Column('email', db.String)
    first_name = db.Column('first_name', db.String)
    last_name = db.Column('last_name', db.String)
    password = db.Column('password', db.String)
    user_code = db.Column('user_code', db.String)
    profile_img = db.Column('profile_img', db.String)
    email_confirmed = db.Column('email_confirmed', db.Boolean)

    def __init__(self, username, email, first_name, last_name, password, user_code, profile_img, email_confirmed):
        self.username = username
        self.email = email
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.user_code = user_code
        self.profile_img = profile_img
        self.email_confirmed = email_confirmed
