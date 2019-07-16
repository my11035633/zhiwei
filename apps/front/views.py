from flask import Blueprint,views ,render_template,make_response,request,url_for,session,g,abort
from .forms import SignupForm,SigninForm,ApostForm,CommentForm
from .models import FrontUser
from exts import db
from utils import restful,safeutils
from  ..models import BannersModel,BoardsModel,Aposts,CommentModel,HighlightModel
from .decorators import login_required
from flask_paginate import Pagination ,get_page_parameter
import config
from sqlalchemy.sql import func
import re


bp=Blueprint("front", __name__)

#首页
@bp.route("/")
def index():
    board_id=request.args.get("bd",type=int,default=None)  #取出板块的id
    page = request.args.get(get_page_parameter(), type=int, default=1)  #一页对象
    sort = request.args.get("sort", type=int, default=1)
    banners=BannersModel.query.order_by(BannersModel.priority.desc()).limit(4).all()
    boards=BoardsModel.query.all()
    start=(page-1)*config.PEG_PAGE  #一页开始位置
    end=start+config.PEG_PAGE   #一页结束位置
    posts=None
    total=0
    if sort==1:
        query_obj=Aposts.query.order_by(Aposts.create_time.desc())
    elif sort==2:
        query_obj=db.session.query(Aposts).outerjoin(HighlightModel).order_by(HighlightModel.create_time.desc(),Aposts.create_time.desc())
    elif sort==3:
        query_obj=db.session.query(Aposts).outerjoin(CommentModel).group_by(Aposts.id).order_by(func.count(CommentModel.id).desc(),Aposts.create_time.desc())

    if board_id:  #如果用户点击板块id
        posts=query_obj.filter(Aposts.board_id==board_id).slice(start,end)  #一页显示的帖子数量
        total=query_obj.filter(Aposts.board_id==board_id).count()   #总共帖子的个数
    else:
        posts = query_obj.slice(start, end)   #用户灭有点击板块时的一页帖子个数
        total=query_obj.count()   #总共帖子数量
    pagination=Pagination(bs_version=3 ,page=page,total=total,outer_window=0,inner_window=2)  #出入2个参数
    #第一个：一页帖子个数，第二个：总共的帖子数量，通过这个变量实现分页栏
    context={
        "banners":banners,
        "boards":boards,
        "posts":posts,   #展示一页贴子数量
        "pagination":pagination,
        "current_id":board_id,  #用来实现板块的选中状态
        "sort":sort  #用来实现帖子的选中状态
    }
    return render_template("front/front_index.html",**context)

#注册页面
class SignUP(views.MethodView):
    def get(self):
        return_to=request.referrer  #获取上一个页面url
        if return_to and return_to != request.url and safeutils.is_safe_url(return_to):
            #上一个页面的url存在，且不等于当前的注册页面，且是安全的
            return render_template("front/front_signup.html",return_to=return_to)
            #将上一个页面的url放到html里面，便于ajax取出
        else:
            return render_template("front/front_signup.html")
    def post(self):
        form=SignupForm(request.form)
        if form.validate():
            telephone=request.form.get("telephone")
            username=request.form.get("username")
            password=request.form.get("password")
            user=FrontUser(telephone=telephone,username=username,password=password)
            db.session.add(user )
            db.session.commit()
            return restful.success("注册成功")
        else:
            message=form.errors.popitem()[1][0]
            return restful.paramserror(message )



#登陆页面
class SignIn(views.MethodView):
    def get(self):
        return_to=request.referrer
        if return_to and return_to !=request.url and return_to !=url_for("front.signup") and safeutils.is_safe_url(return_to):
            #之前页面有且部位当前也页面且不为注册页面
            return render_template("front/front_signin.html",return_to=return_to)
        else:
            return render_template("front/front_signin.html")

    def post(self):
        form=SigninForm(request.form)
        if form.validate():
            telephone = request.form.get("telephone")
            password=request.form.get("password")
            remember=request.form.get("remember")
            user=FrontUser.query.filter(FrontUser.telephone==telephone).first()  #从查出对象
            if user and user.check_password(password):  #如果有这个对象且密码匹配成功
                session["front_user_id"]=user.id   #设置session
                if remember:
                    session.permanent=True   #延长session时间
                    return restful.success(message="登陆成功")
            else:
                return restful.paramserror(message="手机或者密码错误")
        else:
            message=form.errors.popitem()[1][0]
            return restful.paramserror(message)






bp.add_url_rule("/signup/",view_func=SignUP.as_view("signup"))
bp.add_url_rule("/signin/",view_func=SignIn.as_view("signin"))



#发布帖子页面
@bp.route("/aposts/",methods=["GET","POST"])
@login_required
def aposts():
    if request.method=="GET":
        boards=BoardsModel.query.all()
        context={
            "boards":boards
        }
        return render_template("front/front_aposts.html",**context)
    else:
        form=ApostForm(request.form)
        if form.validate():
            title=request.form.get("title")
            board_id=request.form.get("board_id")
            content=request.form.get("content")
            image=re.findall("<img.*?(?:>|/>)",content)
            if image:
                image = re.findall("<img.*?(?:>|/>)", content)[0]
                src=re.findall("http.*?\.jpg|http.*?\.png|http.*?\.gif",image)[0]
                boards=BoardsModel.query.filter(BoardsModel.id==board_id).first()
                if boards:
                    post=Aposts(title=title, content=content,image_src=src)
                    post.board=boards   #这里区分append
                #当有两个对象时添加外键用append,当有一个对象调用关系时用=
                    post.author=g.front_user
                    db.session.add(post)
                    db.session.commit()
                    return restful.success()
                else:
                    return  restful.paramserror(message="没有这个板块")
            else:
                boards = BoardsModel.query.filter(BoardsModel.id == board_id).first()
                if boards:
                    post = Aposts(title=title, content=content)
                    post.board = boards  # 这里区分append
                    # 当有两个对象时添加外键用append,当有一个对象调用关系时用=
                    post.author = g.front_user
                    db.session.add(post)
                    db.session.commit()
                    return restful.success()
                else:
                    return restful.paramserror(message="没有这个板块")
        else:
             message=form.errors.popitem()[1][0]
             return restful.paramserror(message)


#帖子详情
@bp.route("/p/<post_id>/")   #给帖子加上了a标签，将帖子id传入进来 ，就可以根据id找到这个帖子
def post_detail(post_id):
    post=Aposts.query.filter(Aposts.id==post_id).first()
    if not post:
        abort(404)
    else:
        return render_template("front/front_postdetail.html",post=post )



#评论详情
@bp.route("/acomment/" ,methods=["post"])
@login_required
def comment():        #取出postid看是否有这个帖子，有则插入评论，没有则返回错误
    form=CommentForm(request.form)
    if form.validate():
        post_id=request.form.get("post_id")
        content=request.form.get("content")
        post=Aposts.query.filter(Aposts.id==post_id).first()
        if post:
            comment=CommentModel(content=content)
            comment.post=post
            comment.author=g.front_user
            db.session.add(comment)
            db.session.commit()
            return restful.success()
        else:
            return restful.paramserror(message="没有这个帖子")
    else:
        message=form.errors.popitem()[1][0]
        return restful.paramserror(message)



#个人主页
@bp.route("/pcenter/")
@login_required
def pcenter():
    return render_template("front/front_pcenter.html")

#增加签名
@bp.route("/asign/",methods=["post"])
@login_required
def asign():
    sign=request.form.get("sign")
    g.front_user.signature=sign
    db.session.commit()
    return restful.success(message="发表签名成功")

#生活
@bp.route("/life/")
def life():
    return render_template("front/front_life.html")



@bp.route("/avatar/",methods=["post"])
def avatar():
    avatar=request.form.get("avatar")
    g.front_user.avatar=avatar
    db.session.commit()
    return restful.success()
