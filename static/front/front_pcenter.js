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
   $(".submit").click(function (event) {
       event.preventDefault();
       var sign=ue.getContent();


       zlajax.post({
           "url":"/asign/",
           "data":{
               "sign":sign
       },
           "success":function (data) {
               if(data["code"]==200){
                    xtalert.alertSuccessToast(data["message"]);
                    setTimeout(function () {
                           window.location.reload();
                    },500)



               }


           }
       })

   })

});

$(function(){
   zlqiniu.setUp({
       "domain":"http://zhiwei-world.com/",
       "browse_btn":"fileinp",
       "uptoken_url": "/c/uptoken/",
       "success": function(up,file,info){
           var filename=file.name;
           zlajax.post({
               "url": "/avatar/",
               "data":{
                   "avatar":filename,
               },
               "success":function (data) {
                   if(data["code"]==200){
                       setTimeout(function() {
                           window.location.reload();
                       },500)

                   }

               }


           })

       }
   })
});