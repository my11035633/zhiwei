$(function () {
   $("#add_boards") .click(function (event) {
       event.preventDefault();
       xtalert.alertOneInput({
           "text":"请输入板块名字",
           "placeholder":"板块名",
           "confirmCallback":function (inputValue) {
               zlajax.post({
                   "url":"/cms/aboards/",
                   "data":{
                       "name":inputValue
                   },
                   "success":function (data) {
                       if(data["code"]==200){
                           window.location.reload();
                       }else{
                           xtalert.alertInfo(data["message"])
                       }

                   },
                   "fail":function (error) {
                       xtalert.alertNetworkError();

                   }
               })


           }
       })

   })

});


$(function () {
    $(".update").click(function (event) {
        event.preventDefault();
        var self=$(this);
        var tr=self.parent().parent();
        var name=tr.attr("data-name");
        var id=tr.attr("data-id");


        xtalert.alertOneInput({
            "text":"请输入板块的名称",
            "placeholder":"板块名称",
            "confirmCallback":function (inputValue) {
                zlajax.post({
                    "url":"/cms/uboards/",
                    "data":{
                        "name":inputValue,
                        "id":id
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

    })
});


$(function () {
   $(".delete").click(function (event) {
        var self=$(this);
        var tr=self.parent().parent();
        var id=tr.attr("data-id");
       event.preventDefault();
       xtalert.alertConfirm({
           "msg":"确定要删除吗?",
           "confirmCallback":function () {
               zlajax.post({
                   "url":"/cms/dboards/",
                   "data":{
                       "id":id
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

   })
});