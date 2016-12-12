from users_table import Users
from wtforms.validators import ValidationError
def is_email_valid(email):
    # Check if the e-mail address already exists in database.
    taken_check = Users.query.filter(Users.email == email)
    count = int( taken_check.count() )
    if count == 0:
        return False
    return True

def user_email(form, field):
    if is_email_valid(field.data):
        raise ValidationError("The e-mail address {} is already taken.".format(field.data))
