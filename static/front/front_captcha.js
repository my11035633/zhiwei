$(function () {
    $("#captcha-image").click(function (event) {
       var self=$(this);
       var src=self.attr("src");
       var newsrc=zlparam.setParam(src,"xx",Math.random());
       self.attr("src",newsrc)



    });
});



$(function () {
    $("#send-smscaptcha").click(function (event) {
        event.preventDefault();
        var self=$(this);
        var telephone=$("input[name=telephone]").val();
        if (!(/^1[345879]\d{9}$/.test(telephone))){
            xtalert.alertInfoToast("请输入正确手机号码");
        }

        zlajax.post({
            "url":"/c/sendcaptcha/",
            "data":{
                "telephone":telephone
            },

            "success":function (data) {
                  if(data["code"]==200){
                      xtalert.alertSuccessToast("发送成功");
                          self.attr("disabled", "disabled");
                      var timeCount = 60;
                      var timer = setInterval(function () {
                          timeCount--;
                          self.text(timeCount);
                          if (timeCount <= 0) {
                              self.removeAttr("disabled");
                              clearInterval(timer);
                              self.text("发送验证码");
                        }
                    } ,1000);


                } else{xtalert.alertInfo(data["message"]);


                }


            },
            "fail":function (error) {
                xtalert.alertNetworkError();
            }
        });

    });

});



$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var telephone_input=$("input[name=telephone]");
        var sms_captcha_input=$("input[name=captcha]");
        var username_input=$("input[name=username]");
        var password_input=$("input[name=password]");
        var password2_input=$("input[name=password2]");
        var graph_captcha_input=$("input[name=image_captcha]");

        var telephone=telephone_input.val();
        var sms_captcha=sms_captcha_input.val();
        var username=username_input.val();
        var password=password_input.val();
        var password2=password2_input.val();
        var graph_captcha=graph_captcha_input.val();

        zlajax.post({
            "url":"/signup/",
            "data":{
                "telephone":telephone,
                "sms_captcha":sms_captcha,
                "username":username,
                "password":password,
                "password2":password2,
                "graph_captcha":graph_captcha
            },
            "success":function (data) {
                if(data["code"]==200){
                    var return_to=$("#return_to_span").text();
                    if(return_to){
                        window.location=return_to;
                    }else{
                        window.location="/signin/"
                    }

                }else{
                    xtalert.alertInfo(data["message"]);
                }

            },
            "fail":function (error) {
                xtalert.alertNetworkError()

            }
        })

    })

});