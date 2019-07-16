from wtforms import Form, StringField,IntegerField
from wtforms.validators import EqualTo,Regexp,ValidationError,InputRequired
from utils import cache

class SignupForm(Form):
    #先匹配格式是否正确
    telephone=StringField(validators=[Regexp(r"1[354789]\d{9}", message="请输入正确格式的手机号")])
    sms_captcha=StringField(validators=[Regexp(r"\w{4}",message="请输入正确格式的验证码")])
    #任意0-9a-zA-Z的组合4位数
    username=StringField(validators=[Regexp(r".{2,20}",message="请输入正确格式的名字")])
    password=StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}",message="请输入正确的格式的密码")])
    password2=StringField(validators=[EqualTo("password",message="两次密码不一致")])
    graph_captcha=StringField(validators=[Regexp(r"\w{4}",message="请输入正确的验证码")])


    #再匹短信验证码与图形验证码是否正确

    def validate_sms_captcha(self,field):
        sms_captcha=field.data
        mobile=self.telephone.data


        sms_captcha_mem=cache.get(mobile)
        print(sms_captcha_mem)
        if not sms_captcha or sms_captcha.lower() != sms_captcha_mem.lower():
            raise ValidationError(message="短信验证码不一致")

    def validate_graph_captcha(self,field):
        grap_captcha=field.data
        grap_captcha_mem=cache.get(grap_captcha.lower())
        #以用户提交上来的值到mem中取值，如果能取出来则正确的
        if not grap_captcha_mem:
            raise ValidationError(message="图形验证码不匹配")


class SigninForm(Form):
    telephone = StringField(validators=[Regexp(r"1[354789]\d{9}", message="请输入正确格式的手机号")])
    password = StringField(validators=[Regexp(r"[0-9a-zA-Z_\.]{6,20}", message="请输入正确的格式的密码")])
    remember=StringField()

class ApostForm(Form):
    title=StringField(validators=[InputRequired(message="请输入标题")])
    board_id=IntegerField(validators=[InputRequired(message="请输入板块名")])
    content=StringField(validators=[InputRequired(message="请输入内容")])


#评论验证
class CommentForm(Form):
    content=StringField(validators=[InputRequired(message="请输入评论内容")])
    post_id=IntegerField(validators=[InputRequired(message="没有帖子")])
