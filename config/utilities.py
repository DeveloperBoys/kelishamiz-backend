import re
from rest_framework.exceptions import ValidationError

email_regex = re.compile(
    r"([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\"([]!#-[^-~ \t]|(\\[\t -~]))+\")@([-!#-'*+/-9=?A-Z^-~]+(\.[-!#-'*+/-9=?A-Z^-~]+)*|\[[\t -Z^-~]*])")
phone_regex = re.compile(r"^998([378]{2}|(9[013-57-9]))\d{7}$")
username_regex = r"^[a-zA-Z0-9_-]+$"


def check_phone(phone):
    if re.fullmatch(phone_regex, phone):
        phone = "phone"
    else:
        data = {
            "success": False,
            'message': "Your phone number is incorrect"
        }
        raise ValidationError(data)

    return phone


def check_user_type(user_input):
    if re.fullmatch(phone_regex, user_input):
        user_input = "phone"
    elif re.fullmatch(username_regex, user_input):
        user_input = "username"
    else:
        data = {
            "success": False,
            'message': "Your phone number is incorrect"
        }
        raise ValidationError(data)

    return user_input
