var DELETE_ID;
var EDIT_ID;
$(function () {
    const nav = document.querySelector('#bs-example-navbar-collapse-1');
    const lis = nav.querySelectorAll('li');
    lis[1].classList.add('active');
    // 不同的座位类型显示不同的标签颜色
    const seatTypes = document.querySelectorAll('#seatType');
    for (let i = 0; i < seatTypes.length; i++) {
        if (seatTypes[i].innerHTML === "休闲区") {
            seatTypes[i].className = 'label label-primary';
        } else if (seatTypes[i].innerHTML === "阅读区") {
            seatTypes[i].className = 'label label-success';
        } else {
            seatTypes[i].className = 'label label-info';
        }
    }

    bindBtnAddEvent();           // 执行显示模态框
    bindBtnSaveEvent();          // 执行数据提交
    bindBtnDeleteEvent();        // 执行删除对话框
    bindBtnConfirmDeleteEvent();  // 提交数据进行删除
    bindBtnEditEvent();          // 编辑数据

})
function bindBtnAddEvent(){
    $('#btnAdd').click(function (){
        // 将正在编辑的座位置为空
        EDIT_ID = undefined;

        // 需要清空对话框的数据
        $('#PostForm')[0].reset();
        // 点击按钮后，显示模态框
        $('#myModalLabel').text("新建座位");
        $('#btnSave').text("完成创建");
        // 需要删除不可选属性
        $('#id_seatId')[0].removeAttribute('disabled');
        // 显示模态框
        $("#myModal").modal('show');
    })
}
function bindBtnSaveEvent(){
    $('#btnSave').click(function (){

        //清除所有的错误信息
        $(".error-msg").empty();
        // 判断EDIT_ID是否为空
        if(EDIT_ID){
            // 编辑
            doEdit();
        }else {
            // 新建
            doAdd();
        }
    })
}
function doAdd(){
    $.ajax({
            url: '/admin/seat_save/',
            type: 'post',
            data: $('#PostForm').serialize(),
            dataType: 'JSON',
            success: function (res){
                if(res.status) {
                    // alert("创建成功");
                    // 清空表单, PostForm是jQuery对象，("#PostForm")[0]是DOM元素
                    $("#PostForm")[0].reset();
                    // 关闭模态框
                    $("#myModal").modal('hide');
                    window.location.reload();
                }else{
                    // 显示错误信息
                    $.each(res.error, function (name, error_list){
                        $("#id_"+name).next().text(error_list[0])  // 循环输入
                    })
                }

            }
        })
}
function doEdit(){
     $.ajax({
            url: '/admin/seat_edit/' + "?seatId=" + EDIT_ID,
            type: 'post',
            data: $('#PostForm').serialize(),
            dataType: 'JSON',
            success: function (res){
                if(res.status) {
                    // alert("创建成功");
                    // 清空表单, PostForm是jQuery对象，("#PostForm")[0]是DOM元素
                    $("#PostForm")[0].reset();
                    // 关闭模态框
                    $("#myModal").modal('hide');
                    window.location.reload();
                }else{
                    // if(res.tips){
                    //     alert(res.tips);
                    // }else {
                    //     // 显示错误信息
                    //     $.each(res.error, function (name, error_list){
                    //         $("#id_"+name).next().text(error_list[0])  // 循环输入
                    //     });
                    // }
                    alert("数据错误！");
                }

            }
        })
}
function bindBtnDeleteEvent(){
    $('.btn-delete').click(function (){
        $("#deleteModal").modal("show");
        // 获取需要删除的座位Id，将座位Id赋值给DELETE_ID
        DELETE_ID = $(this).attr("uid");
    })
}
function bindBtnConfirmDeleteEvent(){
    $('#ConfirmDelete').click(function (){
        // 提交到后台进行删除
        $.ajax({
            url: '/admin/seat_del/',
            type: 'get',
            dataType: 'JSON',
            data: {
                'seatId': DELETE_ID,
            },
            success: function (res){
                if(res.status){
                    $("#deleteModal").modal("hide");
                    window.location.reload();
                }else{
                    alert(res.result);
                }

            }

        })
    })
}

function bindBtnEditEvent(){
    $('.btn-edit').click(function (){
        $('#PostForm')[0].reset();
        $('#myModalLabel').text("修改座位");
        $('#btnSave').text("确认修改");
        // 获取原先的数据
        var uid = $(this).attr("uid");
        EDIT_ID = uid;
        $.ajax({
            url: '/admin/seat_info/',
            type: 'get',
            dataType: "JSON",
            data: {
                'seatId':  uid,
            },
            success: function (res){
                if(res.status){
                    // 将数据填充到模态框中
                    $.each(res.data, function (name, information){
                        $("#id_"+name).val(information);
                    })

                    // 显示模态框
                    $("#myModal").modal('show');
                    // 前端不允许管理员修改座位编号
                    $('#id_seatId')[0].setAttribute("disabled","disabled");
                }else {
                    alert(res.result);
                }
            }
        })


    })
}
