$(function () {
    $("#captcha-btn").click(function (event) {
        event.preventDefault();
        var email=$("input[name=email]").val();

        zlajax.get({
            "url":"/cms/captcha/",
            "data":{
                "email":email
            },
            "success":function (data) {
               if(data["code"]==200){
                   xtalert.alertSuccessToast(data["message"])
               }else{
                   xtalert.alertInfo(data["message"]);
               }

            },
            "fail":function (error) {
               xtalert.alertNetworkError();

            }
        });

    });

});

$(function () {
    $("#atonce").click(function (event) {
        event.preventDefault();
        var captchav=$("input[name=captcha]");
        var emailv=$("input[name=email]");

        var captcha=captchav.val();
        var email=emailv.val();

        zlajax.post({
            "url":"/cms/resetemail/",
            "data":{
                "email":email,
                "captcha":captcha
            },
            "success":function (data) {
                if(data["code"]==200){
                    xtalert.alertSuccessToast(data["message"]);
                }else{
                    xtalert.alertInfo(data["message"])
                }

            },
            "fail":function (error) {
                xtalert.alertNetworkError()

            }
        });
    });

});