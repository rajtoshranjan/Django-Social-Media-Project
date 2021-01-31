$(function () {
  $('[data-toggle="popover"]').popover()
})

var is_login = false;

  $.ajax({
    url: "/user/islogin",
    type: "GET",
    success: function (result) {
        if(result.is_login)
            // console.log(result)
            is_login = true
    },
    error: function () {
        console.log(false);
    }});



const showNotifications = () => {
    if(is_login)
        $.ajax({
            url: "/user/notifications",
            type: "GET",
            success: function (result) {
                data = JSON.parse(result.data);
                elms = "";
                for (noti in data){
                    elms += `<p class="p-0"><a class"m-0 p-0" href="${data[noti].fields.link}">${data[noti].fields.message}</a></p><hr class="m-0 p-0"/>`;
                }
                // $('#notifications').popover({
                //   content: elms    
                // });
                document.getElementById('notifications').innerHTML=elms;
                $('#clear_notifications').click(clearNotification);
            },
            error: function () {
                console.log(false);
            }});
}

const clearNotification = () =>{
    console.log('clearing notifications ...')
    if(is_login)
     $.ajax({
        url: "/user/notifications/clear",
        type: "POST",
        success: function (result) {
            document.getElementById('notifications').innerHTML="<b class='text-center'>Empty</b>";
        },
        error: function () {
            console.log(false);
        }});
}