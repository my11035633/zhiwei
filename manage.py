from flask_script import Manager
from flask_migrate import Migrate, MigrateCommand
from app import app
from exts import db
from apps.cms import models as cms_models
from apps.front import models as front_models
from apps.models import BoardsModel,Aposts,CommentModel, HighlightModel



manager=Manager(app)
Migrate(app,db)
manager.add_command("db",MigrateCommand)
CMSUser=cms_models.CMSUser
CMSRole=cms_models.CMSRole
CMSPermission=cms_models.CMSPermission
FrontUser=front_models.FrontUser


@manager.option("-u", "--username",dest="username")
@manager.option("-p","--password", dest="password")
@manager.option("-e","--email",dest="email")
def create_cms_user(username,password,email):
    user=CMSUser(username=username, password=password, email=email)
    db.session.add(user)
    db.session.commit()
    print("cms用户注册成功")

#定义角色权限表：用到moldes中的角色表，类权限
@manager.command
def create_role():
    #访问者
    visitor=CMSRole(name="访问者",desc="只能操作数据，不能修改")
    visitor.premission=CMSPermission.VISITOR
    #运营角色
    operator=CMSRole(name="运营", desc="管理帖子，个人信息等")
    operator.premission=CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER
    #管理员
    admin=CMSRole(name="管理员",desc="拥有所有权限")
    admin.premission=CMSPermission.VISITOR|CMSPermission.POSTER|CMSPermission.COMMENTER|CMSPermission.FRONTUSER|CMSPermission.BOARDER|CMSPermission.CMSUSER
    #开发者
    developer=CMSRole(name="开发者", desc="开发专用")
    developer.premission=CMSPermission.ALL_PERMISSION
    db.session.add_all([visitor,operator,admin,developer])
    db.session.commit()

#定义用户与角色之间外键关系
@manager.option("-e","--email",dest="email")
@manager.option("-n","--name",dest="name")
def add_user_role(email,name):
    user=CMSUser.query.filter(CMSUser.email==email).first()  #查出一个已经存在的一个用户
    if user:
        role=CMSRole.query.filter(CMSRole.name==name).first() #查出一个角色对象
        if role:
            role.users.append(user)#添加外键关系
            db.session.commit()
            print("添加成功")
        else:
            print("这个角色不存在")
    else:
        print("这个用户不能存在")

@manager.command
def test_permission():
    user=CMSUser.query.filter(CMSUser.username=="张权").first()
    if user.has_permission(CMSPermission.POSTER):
        print("有")
    else:
        print("没有")

#实现向前台用户表中插入数据
@manager.option("-t","--telephone",dest="telephone")
@manager.option("-u","--username",dest="username")
@manager.option("-p","--password",dest="password")
def create_front_user(telephone,username,password):
    user=FrontUser(telephone=telephone,username=username,password=password)
    db.session.add(user)
    db.session.commit()

@manager.command
def create_post_test():
    for x in range(1,255):
        title="标题%s"% x
        content="内容%s"% x
        board=BoardsModel.query.filter(BoardsModel.name=="风向").first()
        author=FrontUser.query.first()
        post=Aposts(title=title,content=content)
        post.board=board
        post.author=author
        db.session.add(post)
        db.session.commit()





if  __name__  ==  '__main__':
    manager.run()
