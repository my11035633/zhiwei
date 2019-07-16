$(function () {
    var ue=UE.getEditor("editor",{
        "serverUrl":"/ueditor/upload",
        "toolbars":[
            [
                "undo",
                "redo",
                "bold",
                "italic",
                "source",
                "blockquote",
                "selectall",
                "frontfamily",
                "insertcode",
                "fontsize",
                "simpleupload",
                "emotion"
            ]
        ]
    });
    window.ue=ue;
});


$(function () {
   $("#submit").click(function (event) {
        event.preventDefault();
        var login=$("#login-request").attr("data-id");
        var content=ue.getContent();
        var post_id=$("#article").attr("data-postid");
        if(!login){
            window.location="/signup/";
        }else{
            zlajax.post({
                "url":"/acomment/",
                "data":{
                    "content":content,
                    "post_id":post_id
                },
                "success":function (data) {
                    if(data["code"]==200){
                        window.location.reload();
                    }else{
                        xtalert.alertInfo(data["message"])


                    }

                }
            })
        }

   })
});