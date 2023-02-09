$(function (){
    // 提交登录请求
    // BtnRequestLogin();
})

function BtnRequestLogin() {
    $('#PostValues').click(function (){
        console.log("点击了登录")
        $.ajax({
            url: 'admin/login/',
            type: 'post',
            dataType: 'JSON',
            data: $('.loginForm').serialize(),
            success: function (res){
                console.log(res.status);
            },
            error: function (res){
                console.log(res)
            }
        })
    })
}