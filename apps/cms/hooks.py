from flask import session,g
from apps.cms.views import bp
from  apps.cms.models import CMSUser,CMSPermission

#钩子函数：用来将登陆的用户名绑定到g对象上
@bp.before_request
def before_request():
    user_id=session.get("CMS_USER_ID")
    user= CMSUser.query.filter(CMSUser.id==user_id).first()   #不要用get（）方法，玄学不解释
    if user:
     g.cms_user=user

@bp.context_processor
def context_processor():
    return {"CMSPermission":CMSPermission}