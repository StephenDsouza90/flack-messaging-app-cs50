from functools import wraps
from flask import redirect, session


def handle_login(f):
    """ Decorate function """

    @wraps(f)
    def wrapper(*args, **kwargs):
        if session.get("username") is None:
            return redirect("/display-name")
        return f(*args, **kwargs)
    return wrapper