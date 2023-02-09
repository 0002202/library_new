$(function (){
    BtnSignIn();
})
function BtnSignIn(){
    $('#loginUp').click(function (){
        $.ajax({
            url: '/login/',
            type: "post",
            dataType: "JSON",
            data: $('#loginUp').serialize(),
            success: function (res){
                console.log(res.code);
                console.log(res.result);
            }
        })
    })

}