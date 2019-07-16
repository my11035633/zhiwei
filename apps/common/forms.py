from wtforms import StringField,Form
from wtforms.validators import Regexp

class SmscaptchaForm(Form):
    telephone=StringField(validators=[Regexp(r"1[345789]\d{9}", message="输入手机号不存在该格式")])



