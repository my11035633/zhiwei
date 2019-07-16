$(function () {
   $("#save-banners").click(function (event) {
       var self=$(this);
       event.preventDefault();
       var banners=$("#myModal");
       var nameinput=$("input[name=name]");
       var imageinput=$("input[name=image_url]");
       var linkinput=$("input[name=link_url]");
       var priorityinput=$("input[name=priority]");
       var submittype=self.attr("data-type");
       var banners_id=self.attr("data-id");

       var name=nameinput.val();
       var image=imageinput.val();
       var linkurl=linkinput.val();
       var priority=priorityinput.val();

       if(!name||!image||!linkurl||!priority){
           xtalert.alertInfo("请输入完整的数据");
       }

       var url="";
       if(submittype=="update"){
           url="/cms/ubanners/";


       }else{
           url="/cms/abanners/";
       }


       zlajax.post({
           "url":url,
           "data":{
               "name":name,
               "image":image,
               "linkurl":linkurl,
               "priority":priority,
               "id":banners_id,
           },
           "success":function (data) {
               if(data["code"]==200){

                   banners.modal("hide");
                   window.location.reload();

               }else{
                   xtalert.alertInfoToast(data["message"])
               }

           },
           "fail":function (error) {
               xtalert.alertNetworkError();

           }
       })


   })

});


$(function () {
   $(".update").click(function (event) {
       event.preventDefault();
       var banners=$("#myModal");
       banners.modal("show");
       var self=$(this);
       var tr=self.parent().parent();
       var name=tr.attr("data-name");
       var image_url=tr.attr("data-image");
       var link_url=tr.attr("data-link");
       var priority=tr.attr("data-priority");

       var nameinput=$("input[name=name]");
       var imageinput=$("input[name=image_url]");
       var linkinput=$("input[name=link_url]");
       var priorityinput=$("input[name=priority]");
       var savetype=$("#save-banners");

       nameinput.val(name );
       imageinput.val(image_url);
       linkinput.val(link_url);
       priorityinput.val(priority);

       savetype.attr("data-type","update");
       savetype.attr("data-id",tr.attr("data-id"));







   })
});


$(function () {
   $(".delete").click(function (event) {
       var self=$(this);
       var tr=self.parent().parent();
       var id=tr.attr("data-id");
       xtalert.alertConfirm({
           "msg":"确定要删除吗?",
           "confirmCallback":function () {
               zlajax.post({
                   "url":"/cms/dbanners/",
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


$(function () {
   zlqiniu.setUp({
       "domain":"http://zhiwei-world.com/",
       "browse_btn":"add_image",
       "uptoken_url":"/c/uptoken/",
       "success":function (up,file,info) {
           var imageinput=$("input[name=image_url]");
           imageinput.val(file.name);
           console.log(file);


       }
   })
});