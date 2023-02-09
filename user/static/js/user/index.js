$(function (){
    const nav = document.querySelector('#bs-example-navbar-collapse-1');
    const lis = nav.querySelectorAll('li');
    lis[0].classList.add('active');

    bindBtnShowInfor();
})
function bindBtnShowInfor() {
    $(".list-group-item").click(function (){
        console.log("点击了按钮");
        // 获取uid传动前端进行展示公告内容
        var uid = $(this).attr('uid');

        // 显示模态框
        $('#'+uid).modal('show');
    })

}