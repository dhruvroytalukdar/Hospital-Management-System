from flask_login import current_user
from flask import redirect, url_for
from functools import wraps


def requires_roles(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated == False:
                return redirect(url_for('home'))
            if current_user.roles not in roles:
                # Redirect the user to an unauthorized notice!
                return redirect(url_for('doctorView'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper


def already_logged_in(*roles):
    def wrapper(f):
        @wraps(f)
        def wrapped(*args, **kwargs):
            if current_user.is_authenticated == True:
                return redirect(url_for('doctorView'))
            return f(*args, **kwargs)
        return wrapped
    return wrapper
