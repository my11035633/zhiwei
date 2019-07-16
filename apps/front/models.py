from exts import db
import shortuuid
import enum
from datetime import datetime
from werkzeug.security import generate_password_hash,check_password_hash
class GenderEnum(enum.Enum):  #定义一个枚举
    MALE=1
    FEMALE=2
    SECRET=3
    UNKNOW=4


class FrontUser(db.Model):
    __tablename__="front_user"
    id=db.Column(db.String(100),primary_key=True, default=shortuuid.uuid)
    telephone=db.Column(db.String(11),nullable=False,unique=True)
    username=db.Column(db.String(100),nullable=False)
    _password=db.Column(db.String(100),nullable=False)
    email=db.Column(db.String(100),unique=True)
    realname=db.Column(db.String(50))
    avatar=db.Column(db.String(100))
    signature=db.Column(db.String(100))
    gender=db.Column(db.Enum(GenderEnum),default=GenderEnum.UNKNOW)  #性别类型是枚举
    join_time=db.Column(db.DateTime,default=datetime.now)

    def __init__(self,*args,**kwargs):
        if "password" in kwargs:
            self.password=kwargs.get("password")
            kwargs.pop("password")
        super(FrontUser,self ).__init__(*args,**kwargs)


    @property
    def password(self):
        return self._password

    @password.setter
    def password(self ,newpwd):
        self._password = generate_password_hash(newpwd)

    def check_password(self,newpwd):
        return check_password_hash(self.password,newpwd)



