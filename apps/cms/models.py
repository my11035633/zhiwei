from exts import db
from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
class CMSUser(db.Model):
    __tablename__="cms_user"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    username=db.Column(db.String(50),nullable=False)
    _password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(50),nullable=False, unique=True)
    join_time=db.Column(db.DateTime, default=datetime.now)

    def __init__(self,username,password,email): #重写了初始化方法，
        self.username=username
        self.password=password #当实例化用password时，到这里调用self.password函数@password.setter
        self.email=email

    @property    #调用密码函数方法
    def password(self):
        return self._password

    @password.setter   #定义设置密码函数方法
    def password(self,raw_password):
       self._password= generate_password_hash(raw_password)  #上面调用函数到这里，然后加密，最后传给模型中的_password

    def check_password(self, raw_password): #定义登陆时核查密码方法
        result=check_password_hash(self.password, raw_password)  #将传入密码与模型密码对比
        return result
#判断用户有多少个权限
    @property
    def permissions(self):
        if not self.roles:   #通过relationship调用，看用户是否在角色表中
            return 0       #不在，返回0
        else:
            all_permissions=0
            for role in self.roles:           #通过relationship调用，拿到一个列表
                permission=role.premission
                all_permissions=permission
            return all_permissions   #返回所有的权限

     #判断是否有否个权限
    def has_permission(self,permission):
        all_permissions=self.permissions       #直接调用上面的函数，拿到这个用户的所有权限
        result=all_permissions&permission==permission  #所有权限与传进的权限与运算，如果与传进来的相等，则有这个权限
        return result  #有这个权限，result为1 ，没有为0

    #判断是否为开发者
    @property
    def is_developer(self):
        return self.has_permission(CMSPermission.ALL_PERMISSION)


 #为了保证密码安全性，对外用password，对内用_password,在实例化对象时还是用password,但是模型中已经变成_password;
 #因此，需要重写init方法。

#定义类权限
class CMSPermission(object):
    # 最高管理权限
    ALL_PERMISSION = 0b11111111
    # 访问者的权限
    VISITOR = 0b00000001
    # 管理帖子的权限
    POSTER = 0b00000010
    # 管理评论的权限
    COMMENTER = 0b00000100
    # 管理板块的权限
    BOARDER = 0b00001000
    # 管理前台的权限
    FRONTUSER = 0b000010000
    # 管理后台的权限
    CMSUSER = 0b00100000
    # 管理管理员的权限
    AOMINER = 0b01000000

#第三方表，用来连接用户表与角色表，多对多关系
cms_role_user=db.Table(
    "cms_role_user",
    db.Column("cms_role_id",db.Integer, db.ForeignKey("cms_role.id"),primary_key=True),
    db.Column("cms_user_id",db.Integer,db.ForeignKey("cms_user.id"),primary_key=True)

)


#角色权限表
class CMSRole(db.Model):
    __tablename__="cms_role"
    id=db.Column(db.Integer,primary_key=True, autoincrement=True)
    name=db.Column(db.String(30),nullable=False)
    desc=db.Column(db.String(100), nullable=False)
    create_time=db.Column(db.DateTime,default=datetime.now)
    premission=db.Column(db.Integer,default=CMSPermission.VISITOR)


    users=db.relationship("CMSUser",backref="roles",secondary=cms_role_user)





