from flask import session ,redirect,url_for,g,render_template
from functools import wraps

def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if session.get("front_user_id"):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("front.signin"))
    return inner

