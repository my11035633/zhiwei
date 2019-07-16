import requests


def send_capt(mobile,captcha):
    url="http://v.juhe.cn/sms/send"
    params={
        "mobile":mobile,
        "tpl_id":141026,
        "tpl_value":"#code#="+captcha,
        "key":"8feede4294c2bea15c96dd5cd6580f1c"
    }
    response=requests.get(url,params=params)
    result=response.json()
    if result["error_code"]==0:
        return True
    else:
        return False