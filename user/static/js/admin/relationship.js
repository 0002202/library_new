var EDIT_USER_ID;
$(function (){
    const nav = document.querySelector('#bs-example-navbar-collapse-1');
    const lis = nav.querySelectorAll('li');
    lis[3].classList.add('active');
    
    // 根据用户状态，加以颜色区分
    const userTypes = document.querySelectorAll('#userType');
    const userSeatId = document.querySelectorAll('#userSeatId');

    for (let i = 0; i < userTypes.length; i++) {
        // if (userSeatId[i].innerHTML === ''){
        //     userSeatId[i].innerHTML = "无数据";
        // }
        if (userTypes[i].innerHTML === "未预约") {
            userTypes[i].className = 'label label-primary';
        } else if (userTypes[i].innerHTML === "已预约") {
            userTypes[i].className = 'label label-success';
        } else {
            userTypes[i].className = 'label label-info';
        }
    }

    BtnResEdit();       // 模态框中显示数据
    BtnResEditSave();   // 将数据进行提交
})
function BtnResEdit() {
        $('.btn-edit').click(function (){
            // 获取原先的数据
            var uid = $(this).attr("uid");
            EDIT_USER_ID = uid;
            $.ajax({
                url: '/admin/user_info/',
                type: 'get',
                dataType: "JSON",
                data: {
                    'userId':  uid,
                },
                success: function (res){
                    if(res.status){
                        $.each(res.data, function (name, information){
                        $("#id_"+name).val(information);
                    })
                        $("#myModal").modal('show');
                        // 前端不允许管理员修改座位编号
                        $('#id_userId')[0].setAttribute("disabled","disabled");
                    }else{
                        alert("数据出错！！！");
                    }
                }
        })
    })
}

function BtnResEditSave() {
    $('#postData').click(function (){
        // 将修改的数据提交到数据库中

        $.ajax({
            url: '/admin/user_edit/' + "?userId=" + EDIT_USER_ID,
            type: 'post',
            dataType: "JSON",
            data: $('#PostForm').serialize(),
            success: function (res){
                if (res.status){
                    console.log(res.result);
                }
            }
        })
        $("#myModal").modal('hide');
        window.location.reload();
    })
}