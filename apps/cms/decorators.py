from flask import session ,redirect,url_for,g
from functools import wraps
def login_required(func):
    @wraps(func)
    def inner(*args,**kwargs):
        if session.get("CMS_USER_ID"):
            return func(*args,**kwargs)
        else:
            return redirect(url_for("cms.login"))
    return inner

#2层装饰器
def permission_required(permission):   #这个仅仅是一个函数
    def outer(func):               #才是真正的装饰器
        @wraps(func)
        def inner(*args,**kwargs):
            if g.cms_user.has_permission(permission):
                return func(*args,**kwargs)
            else:
                return redirect(url_for("cms.index"))
        return inner
    return outer          #返回装饰器的名字