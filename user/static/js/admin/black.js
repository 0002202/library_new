var EDIT_ID;
$(function (){
    const nav = document.querySelector('#bs-example-navbar-collapse-1');
    const lis = nav.querySelectorAll('li');
    lis[0].classList.add('active');

    bindBtnInfoEvent(); // 显示提示框
    bindBtnSaveEvent(); // 保存数据
    bindBtnProlongTimeEvent();  // 延长数据
    bindBtnProlongTimeSaveEvent(); //保存延长数据
    bindBtnDelEvent();  // 删除数据
})

function bindBtnInfoEvent() {
     $("#blackUserBtn").click(function (){
         // 还原模态框
         $('#DataPostForm')[0].reset();
         $(".error-msg").empty();
         // 获取当前时间填入
         let time = new Date();
         $('#createTime').val(time.toLocaleString());


         // 显示模态框
         $("#myModal").modal('show');
     })
}
function bindBtnSaveEvent(){
    $('.btn-save').click(function (){
        // 点击了保存
        console.log("点击了完成")
        $.ajax({
            url: '/admin/black_save/',
            type: 'post',
            dataType: 'JSON',
            data: $('#DataPostForm').serialize(),
            success: function (res) {
                if (res.status) {
                    // 关闭模态框，返回成功信息
                    $("#myModal").modal('hide');
                    window.location.reload();
                }else {
                    // 填充时间错误
                    $('#id_userId').next().text(res.userError);
                    $("#id_cancelTime").next().text(res.timeError);
                    // 显示错误信息
                    $.each(res.error, function (name, error_list) {
                        $("#id_" + name).next().text(error_list[0])  // 循环输入
                    })
                }
            }
        })
    })
}
function bindBtnProlongTimeEvent() {
    $('.prolongTimeBtn').click(function (){
        // 获取数据
        var uid = $(this).attr('uid');
        EDIT_ID = uid;
        $.ajax({
            url: '/admin/black_info/',
            type: 'get',
            dataType: "JSON",
            data: {
                'blackUserId': uid,
            },
            success: function (res){
                if (res.status){
                    // 填入数据
                    $("#userId").val(uid);
                    $("#createTime1").val(res.createTime);
                    $("#cancelTime").val(res.cancelTime);
                    // 显示模态框
                    $('#myModal1').modal('show');
                }else {
                    console.log(res);
                }

            }
        })

    })
}
function bindBtnProlongTimeSaveEvent() {
    $("#prolongTimeBtn").click(function (){
        // 保存修改信息
        $.ajax({
            url: '/admin/black_update/'+'?BlackUserId='+EDIT_ID,
            type: 'post',
            dataType: 'JSON',
            data: $("#prolongTimeForm").serialize(),
            success: function (res){
                if (res.status){
                    // 提示成功信息

                    // 关闭模态框
                    $('#myModal1').modal('hide');
                    window.location.reload();
                }else{
                    $("#prolongTimeSpan").text(res.timeError);
                }
            }
        })

    })
}
function bindBtnDelEvent() {
    $(".btn-del").click(function (){
        // 删除数据
        var uid = $(this).attr('uid');
        $.ajax({
            url: '/admin/black_del/',
            type: 'get',
            dataType: "JSON",
            data: {'blackUserId': uid},
            success: function (res){
                if (res.status){
                    // 增加提示细节
                    window.location.reload();
                }else {
                    console.log(res.result);
                }
            }
        })

    })
}