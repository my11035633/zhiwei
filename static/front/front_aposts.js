$(function () {
   var ue=UE.getEditor("editor",{
       "serverUrl":"/ueditor/upload/"
   });

   $("#submitposts").click(function (event) {
       event.preventDefault();

       var titleinput=$("input[name=title]");
       var board_idinput=$("select[name=board-id]");
       var content=ue.getContent();
       
       var title=titleinput.val();
       var board_id=board_idinput.val();

       zlajax.post({
           "url":"/aposts/",
           "data":{
               "title":title,
               "board_id":board_id,
               "content":content,
           },
           "success":function (data) {
               if(data["code"]==200){
                     xtalert.alertConfirm({
                   "msg":"恭喜，发布成功",
                   "cancelText":"回到首页",
                   "confirmText":"再发一篇",
                   "cancelCallback":function () {
                       window.location="/";

                   },
                   "confirmCallback":function () {
                       titleinput.val("");
                       ue.setContent("");

                   }
               })

               }else{
                   xtalert.alertInfo(data["message"]);
               }


           }
       })

   })




});