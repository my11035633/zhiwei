$(function () {
   $(".highlight-btn").click(function (event) {
       event.preventDefault();
       var self=$(this);
       var tr=self.parent().parent();
       var post_id=tr.attr("data-id");
       var highlight=parseInt(tr.attr("data-highlight"));

       if(highlight){
           url="/cms/uhigh/"
       }else{
           url="/cms/ahigh/"
       }
       zlajax.post({
           "url":url,
           "data":{
               "post_id":post_id
           },
           "success":function (data) {
               if(data["code"]==200){
                   xtalert.alertSuccessToast(data["message"]);
                   setTimeout(function () {
                       window.location.reload();

                   },300)

               }else{
                   xtalert.alertInfo(data["message"])
               }

           }
       })


   })
});


$(function () {
   $(".delete").click(function (event) {
       event.preventDefault();
       var self=$(this);
       var tr=self.parent().parent();
       var post_id=tr.attr("data-id");
       zlajax.post({
           "url":"/cms/deletehigh/",
           "data":{
               "post_id":post_id
           },
           "success":function (data) {
               if(data["code"]==200){
                   xtalert.alertSuccessToast(data["message"])
                   setTimeout(function () {
                       window.location.reload();

                   },500)
               }else{
                   xtalert.alertInfoToast(data["message"])
               }

           }
       })


   })

});