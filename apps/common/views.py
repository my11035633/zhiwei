from flask import Blueprint,request ,make_response,jsonify,g
from utils import send_captcha
from exts import db
from utils import restful
from .forms import SmscaptchaForm
from utils.captcha.xtcaptcha import Captcha
from io import BytesIO
from utils import cache
import qiniu
from ..front import hooks




bp=Blueprint("common", __name__,url_prefix="/c")

@bp.route("/common/")
def index():
    return "common"

#发送短信验证码
@bp.route("/sendcaptcha/" ,methods=["POST"])
def send():
    form=SmscaptchaForm(request.form )
    if form.validate():
        mobile=request.form.get("telephone")
        captcha = Captcha.gene_text()    #调用验证码内容
        if send_captcha.send_capt(mobile, captcha): #调用封装好的短信发送函数
            cache.set(mobile,captcha)           #将短信验证码存储在memcache中
            return restful.success(message="发送成功")  #成功直接调用不传参数
        else:
            return restful.paramserror(message="发送失败")
    else:
        message=form.errors.popitem()[1][0]
        return restful.paramserror(message)


#获取图形验证码
@bp.route("/captcha/")
def graph_captcha():
    text,image=Captcha.gene_code()      #调用类方法，拿到验证码
    cache.set(text.lower(),text.lower()) #将图形验证码存储在memcache，内容全部变成小写
    out=BytesIO()            #初始化二进制流对像
    image.save(out,"png")    #将验证码存储在二进制流中，因为单纯的数据是不能被计算机识别的，只有先存储在二进制流中，并以png格式
    out.seek(0)         #保存后将指针移到开始位置，方便后面读取数据
    resp=make_response(out.read())        #从二进制流中读取数据以response对象
    resp.content_type="/image/png"        #制定response数据类型
    return resp    #返回对象


#七牛云接口
@bp.route("/uptoken/")
def uptoken():
    access_key="RGJIrhTPY74Wo4SZw8OTzSnxTvLIu6lbPzrTu2xr"
    secret_key="j6AbvPSo8tFsNu6Hwoh9X2wyFGHjUvNNswkUq00t"
    q=qiniu.Auth(access_key,secret_key)
    bucket="mybaobao"
    token=q.upload_token(bucket)
    return jsonify({"uptoken":token})

