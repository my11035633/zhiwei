from flask import Blueprint,render_template, views,request,redirect,url_for,session,g,jsonify
from apps.cms.forms import LoginForm,ResetPaw,ResetEmail,BannersForm,BannersUpForm,BoardsForm,UboardsForm
from apps.cms.models import CMSUser,CMSPermission
from apps.cms.decorators import  login_required, permission_required
from exts import db ,mail
from utils import restful, cache
from flask_mail import Message
import string
import random
from apps.models import BannersModel,BoardsModel,Aposts,HighlightModel
from flask_paginate import Pagination,get_page_parameter
import config
from config import CMS_USER_ID
bp=Blueprint("cms", __name__,url_prefix="/cms")

@bp.route("/")
@login_required
def index():
    return  render_template("cms/base.cms.html")


#注销功能实现
@bp.route("/logout/")
def logout():
    session.clear() #清楚所有session
    return redirect(url_for("cms.login"))   #反转时一定要注意加上蓝图名字



#登陆的类视图：一般get,post请求用类视图写比较简单，html及css模板从bootstrap拷贝。
class LoginView(views.MethodView):

    def get(self, message=None):  #message=None,正向渲染模板message没有值
        return render_template("cms/cms_login.html",message=message) #文件在cms文件夹下面

    def post(self):
        form =LoginForm(request.form)
        if form.validate():
            email=request.form.get("email")
            password=request.form.get("password")
            remmber=request.form.get("remmber")
            user=CMSUser.query.filter(CMSUser.email==email).first()
            # 重点：以后全部用filter,不要用filter_by,因为filter_by里面传的是关键字参数，不是等于关系,易错
            if user and user.check_password(password):
                session["CMS_USER_ID"]=user.id    #设置session必须在配置文件中加入密钥
                if remmber:
                    session.permanent=True
                    return redirect(url_for("cms.index"))  #蓝图中反转必须加上蓝图名字
                else:
                    return redirect(url_for("cms.index"))
            else:
                return self.get(message="邮箱或者密码错误")  #如果用户不存在，返回错误
        else:
            message=form.errors.popitem()[1][0]
            #如果forms验证不通过，说明密码或者邮箱格式不对
            #所有错误类型都是存在form.errors字典中
            #列：form.errors={"password":["密码错误"]}，通过popitem（），取出：（"password",["密码错误"]）
            return self.get(message)   #调用get方法实现本页面的跳转

bp.add_url_rule("/login/",view_func=LoginView.as_view("login"))



#定义一个个人信息页面
@bp.route("/profile/")
@login_required
def profile():
    return render_template("cms/cms_profile.html")
#注意：在html页面中{{}}里面必须写内容，不能空着，否则会报错。


#邮箱的发送
@bp.route("/captcha/")
def send_captcha():
    email=request.args.get("email")  #取出ajax提交上来的数据
    source=list(string.ascii_letters)
    #string.ascii_letters是一个字符串类型 ： "a-z/A-Z ",然后转换成列表形式：["a"...."Z"]
    source.extend(map(lambda x:str(x),range(0,10)))
    #map(函数，可迭代对象)，它会将可迭代对象执行前面函数，返回值放到一个列表中；此代码最后拿到
    #["0"...."9"],然后extend方法更新到source列表中
    captcha="".join(random.sample(source, 6))
    #random中sample方法随机在列表中选区几位数；join将列表拼接成字符串，就得到了验证码
    message=Message("之微论坛",recipients=[email],body="你的验证码是:{}".format(captcha))
    try:  #捕获一下异常
        mail.send(message)
    except:
        return restful.servererror()
    cache.set(email,captcha )   #将邮箱与验证码设置到memcache里面，方便在form表单中调用，判断与
    #提交上来的验证码是否一致
    return restful.success("邮件已发送，请注意查收")




#写修改密码页面
class ResetPwdView(views.MethodView):

     def get(self):
        return render_template("cms/cms_resetpaw.html")

     def post(self):
         form=ResetPaw(request.form)
         if form.validate():
             oldpaw=request.form.get("oldpaw")
             newpaw=request.form.get("newpaw")
             user=g.cms_user   #通过g对象拿到登陆用户的对象
             if user.check_password(oldpaw):   #调用配置文件中核查函数，看旧密码是否存在
                 user.password=newpaw   #更改密码
                 db.session.commit()
                 return restful.success("密码修改成功")
             else:
                 return restful.paramserror("旧密码错误")  #在utils中对返回jsonify进行封装
         else:
             message=form.errors.popitem()[1][0]   #取出错误信息
             print(message)
             return restful.paramserror("两次密码不一致")

bp.add_url_rule("/resetpwd/", view_func=ResetPwdView.as_view("resetpwd"))

#修改邮箱页面
class ResetEmailView(views.MethodView):
    decorators=[login_required]
    def get(self):
        return render_template("cms/cms_resetemail.html")

    def post(self):
        form=ResetEmail(request.form )
        if form.validate():
            email=request.form.get("email")
            g.cms_user.email=email
            db.session.commit()
            return restful.success("邮箱修改成功")
        else:
            message=form.errors.popitem[1][0]
            return restful.paramserror(message )


bp.add_url_rule("/resetemail/", view_func=ResetEmailView.as_view("resetemail"))

#轮播图插入
@bp.route("/banners/")
@login_required
def  banners():
    banners=BannersModel.query.all()   #从表中取出所有数据渲染到模板中，用FOR 循环遍历出
    return render_template("cms/cms_banners.html",banners=banners)

@bp.route("/abanners/",methods=["post"])  #插入数据库将轮播图信息
@login_required
def abanners():
    form=BannersForm(request.form)
    if form.validate():
        name=request.form.get("name")
        image=request.form.get("image")
        linkurl=request.form.get("linkurl")
        priority=request.form.get("priority")
        banners=BannersModel(name=name,image_url=image,link_url=linkurl,priority=priority)
        db.session.add(banners)
        db.session.commit()
        return restful.success()
    else:
        message=form.errors.popitem()[1][0]
        return restful.paramserror(message)

#轮播图修改编辑
@bp.route("/ubanners/",methods=["post"])
@login_required
def ubanners():
    form=BannersUpForm(request.form)
    if form.validate():
        name = request.form.get("name")
        image = request.form.get("image")
        linkurl = request.form.get("linkurl")
        priority = request.form.get("priority")
        print(priority)
        id=request.form.get("id")
        banners=BannersModel.query.filter(BannersModel.id==id).first()
        if banners:
            banners.name=name
            banners.image_url = image
            banners.link_url = linkurl
            banners.priority = priority
            db.session.commit()
            return restful.success()
        else:
            return restful.paramserror(message="没有这个轮播图")
    else:
        message=form.errors.popitem()[1][0]
        return restful.paramserror(message)

#轮播图删除
@bp.route("/dbanners/",methods=["post"])
def dbanners():
    id=request.form.get("id")
    print(id)
    banner=BannersModel.query.filter(BannersModel.id==id).first()
    if banner:
        db.session.delete(banner)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramserror(message="删除失败")

#板块插入
@bp.route("/aboards/", methods=["post"])
@login_required
@permission_required(CMSPermission.BOARDER)
def aboards():
    form=BoardsForm(request.form)
    if form.validate():
        name=request.form.get("name")
        boards=BoardsModel(name=name)
        db.session.add(boards)
        db.session.commit()
        return restful.success()
    else:
        message=form.errors.popitem()[1][0]
        restful.paramserror(message)


#编辑板块
@bp.route("/uboards/",methods=["post"])
@login_required
@permission_required(CMSPermission.BOARDER)
def uboards():
    form=UboardsForm(request.form)
    if form.validate():
        id=request.form.get("id")
        name=request.form.get("name")
        boards=BoardsModel.query.filter(BoardsModel.id==id).first() #查是否有这个对象
        if boards:  #有则编辑
            boards.name=name
            db.session.commit()
            return restful.success()
        else:
            return restful.paramserror(message="没有这个数据")
    else:
        message=form.errors.popitem()[1][0]
        return restful.paramserror(message)


#删除板块
@bp.route("/dboards/",methods=["post"])
@login_required
@permission_required(CMSPermission.BOARDER)
def dboards():
    id=request.form.get("id")   #删除就不需要到form验证了，直接删就可以了
    boards=BoardsModel.query.filter(BoardsModel.id==id).first()
    if boards:
        db.session.delete(boards)
        db.session.commit()
        return restful.success()
    else:
        return restful.paramserror(message="没有这个数据")
















#帖子呈现的页面
@bp.route("/posts/")
@login_required
@permission_required(CMSPermission.VISITOR)    #2层装饰器：先调用permission_required()函数，拿到真正的装饰器名字
#他的目的就是为了传参，将权限传进去
def posts():
    page=request.args.get(get_page_parameter(),type=int,default=1)
    start=(page-1)*config.PEG_PAGE
    end=start+config.PEG_PAGE
    posts_list=Aposts.query.order_by(Aposts.create_time.desc()).slice(start,end)
    total=Aposts.query.count()
    pagination=Pagination(bs_version=3,page=page,total=total,outer_window=0,inner_window=2)
    context={
        "pagination":pagination,
        "posts_list":posts_list
    }
    return render_template("cms/cms_posts.html",**context)



#加精
@bp.route("/ahigh/" ,methods=["post"])
@login_required
@permission_required(CMSPermission.VISITOR)
def ahigh():
    post_id=request.form.get("post_id")
    post=Aposts.query.filter(Aposts.id==post_id).first()
    if post:
        highlight=HighlightModel()
        highlight.post=post
        db.session.add(highlight)
        db.session.commit()
        return restful.success(message="加精成功")
    else:
        return restful.paramserror(message="没有这个帖子")


#取消加精
@bp.route("/uhigh/" ,methods=["post"])
@login_required
@permission_required(CMSPermission.VISITOR)
def uhigh():
    post_id=request.form.get("post_id")
    post=Aposts.query.filter(Aposts.id==post_id).first()
    if post:
        highlight=HighlightModel.query.filter(HighlightModel.post_id==post_id).first()
        db.session.delete(highlight)
        db.session.commit()
        return restful.success(message="取消加精成功")
    else:
        return restful.paramserror(message="没有这个帖子")



#删除帖子
@bp.route("/deletehigh/" ,methods=["post"])
@login_required
@permission_required(CMSPermission.VISITOR)
def deletehigh():
    post_id=request.form.get("post_id")
    post=Aposts.query.filter(Aposts.id==post_id).first()
    if post:
        db.session.delete(post)
        db.session.commit()
        return restful.success(message="删除成功")
    else:
        return restful.paramserror(message="网页在加载中")


@bp.route("/comments/")
@login_required
@permission_required(CMSPermission.COMMENTER)
def comments():
    return render_template("cms/cms_comments.html")

@bp.route("/boards/")
@login_required
@permission_required(CMSPermission.BOARDER)
def boards():
    boards=BoardsModel.query.all()
    context={
        "boards":boards
    }
    return render_template("cms/cms_boards.html",**context)

@bp.route("/fusers/")
@login_required
@permission_required(CMSPermission.FRONTUSER)
def fusers():
    return render_template("cms/cms_fusers.html")

@bp.route("/cusers/")
@login_required
@permission_required(CMSPermission.CMSUSER)
def cusers():
    return render_template("cms/cms_cusers.html")

@bp.route("/croles/")
@login_required
@permission_required(CMSPermission.ALL_PERMISSION)
def croles():
    return render_template("cms/cms_croles.html")

