$(function () {
    $("#submit").click(function (event) {
        event.preventDefault();
        var oldpaw = $("input[name=oldpaw]").val();
        var newpaw = $("input[name=newpaw]").val();
        var oldpaw2 = $("input[name=oldpaw2]").val();

        zlajax.post(
            {
                "url": "/cms/resetpwd/",
                "data": {
                    "oldpaw": oldpaw,
                    "newpaw": newpaw,
                    "oldpaw2": oldpaw2
                },
                "success": function (data) {
                    if (data["code"] == 200) {
                        xtalert.alertSuccessToast("恭喜，密码修改成功");
                        $("input[name=oldpaw]").val("");
                        $("input[name=newpaw]").val("");
                        $("input[name=oldpaw2]").val("");
                    } else {
                        var message = data["message"];
                        xtalert.alertInfo(message)

                    }

                },
                "fail":  function (error) {
                     xtalert.alertNetworkError();



                }

            });
    });

} );