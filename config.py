############################################################################
#flask details and configuation
############################################################################
import flask
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from werkzeug.utils import secure_filename
from flask_mail import Mail

app = flask.Flask(__name__)
#password hashing
bcrypt = Bcrypt(app)

#needed to send emails for confirmation emails and password reset requests
mail = Mail(app)

app.config.update(
    #EMAIL SETTINGS
    MAIL_SERVER='smtp.gmail.com',
    MAIL_PORT=587,
    MAIL_USE_SSL=False,
    MAIL_USE_TLS=True,
    MAIL_USERNAME = 'YourEmail@gmail.com',
    MAIL_PASSWORD = 'YourPassword123'
)

mail = Mail(app)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0
app.config['SECRET_KEY'] = 'GENERATE_RANDOM_CODE'

ts = URLSafeTimedSerializer(app.config["SECRET_KEY"])

app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/database' #enter your database info
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
