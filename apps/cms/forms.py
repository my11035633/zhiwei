from wtforms import Form , StringField,IntegerField,ValidationError
from wtforms.validators import Email , InputRequired,Length,EqualTo
from flask import g
from utils import cache
class LoginForm (Form):
    email=StringField(validators=[Email(message="邮箱输入有误"),InputRequired(message=("请输入邮箱"))])
    password=StringField(validators=[Length(6,12,message="请输入正确的密码")])
    remmber=IntegerField()


class ResetPaw(Form):
    oldpaw=StringField(validators=[Length(6,12,message="请输入正确的密码")])
    newpaw=StringField(validators=[Length(6,12,message="请输入正确的密码")])
    oldpaw2=StringField(validators=[EqualTo("newpaw",message="确认密码不一致")])

class ResetEmail(Form ):
    email=StringField(validators=[Email(message="邮箱格式不对")])
    captcha=StringField(validators=[Length(min=6, max=6,message="验证码长度不对")])

#自定义邮箱验证：用来验证邮箱不能与之前的一样
    def validate_email(self,field):
        email=field.data   #取出提交上来的email
        if email==g.cms_user.email:    #判断与之前邮箱是否一样
            raise ValidationError("不能用原先的邮箱")

    def validate_captcha(self, field):
        email=self.email.data   #取出邮箱，通过之前获取验证码提交上来的邮箱来取
        captcha=field.data    #取出这次提交上来的验证码
        captcha_send=cache.get(email)  #取出memcache中的验证码
        if not captcha and captcha.lower()!=captcha_send.lower():  #比较2个验证码
            raise ValidationError("验证码错误")

#轮播图插入验证
class BannersForm(Form):
    name=StringField(validators=[InputRequired(message="请输入图片的名字")])
    image = StringField(validators=[InputRequired(message="请输入图片地址")])
    linkurl = StringField(validators=[InputRequired(message="请输入跳转地址的名字")])
    priority= IntegerField(validators=[InputRequired(message="请输入图权重")])

#轮播图编辑验证
class BannersUpForm(BannersForm):
    id=IntegerField(validators=[InputRequired(message="请输入轮播图ID")])

#板块的插入验证
class BoardsForm(Form):
    name=StringField(validators=[InputRequired(message="请输入名字")])


#验证编辑板块
class UboardsForm(Form):
    name = StringField(validators=[InputRequired(message="请输入名字")])
    id=IntegerField(validators=[InputRequired(message="请输入id")])






