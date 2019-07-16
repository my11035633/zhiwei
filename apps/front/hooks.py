from flask import session,g,render_template
from apps.front.views import bp
from .models import FrontUser


#钩子函数：用来将登陆的用户名绑定到g对象上
@bp.before_request
def before_request():
    user_id=session.get("front_user_id")
    user= FrontUser.query.filter(FrontUser.id==user_id).first()   #不要用get（）方法，玄学不解释
    if user:
        g.front_user=user


#主动抛出异常钩子函数
@bp.errorhandler(404)
def errorhander(error):
    return render_template("front/front_404.html"),404
