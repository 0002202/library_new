var DELETE_ID;
var EDIT_ID;
$(function (){
    const nav = document.querySelector('#bs-example-navbar-collapse-1');
    const lis = nav.querySelectorAll('li');
    lis[2].classList.add('active');

    BtnAddInforEvent();     // 新增公告
    BtnSaveInforEvent();     // 保存数据
    BtnDeleteEvent();        // 获取公告ID
    BtnDelInforEvent();      // 删除公告
    BtnInfoInforEvent();     // 获取公告信息

    BtnShowInforEvent();     // 查看公告内容
})

function BtnAddInforEvent() {
        $('#AddInfor').click(function (){
            $('#myModalLabel').text("创建公告");
            $('#postData1').text("完成创建");
            // 将正在编辑的座位置为空
            EDIT_ID = undefined;
            $('#PostForm1')[0].reset();      // 需要清空对话框的数据
            // 填入当前登录用户
            // $.ajax({
            //     url: '/admin/infor_return/',
            //     type: 'get',
            //     dataType: 'JSON',
            //     success: function (res){
            //         // 填入框中
            //         console.log(res.name);
            //         $('#id_createName').val(res.name);
            //         $('#myModal1').modal('show');   // 显示模态框
            //     }
            // })
            $('#myModal1').modal('show');
        })
    }

// function BtnSaveInforEvent() {
//
//         $('#postData1').click(function (){
//
//             // 向后端发送数据
//             $.ajax({
//                 url: '/admin/infor_save/',
//                 type: 'post',
//                 dataType: 'JSON',
//                 data: $('#PostForm1').serialize(),
//
//                 success: function (res){
//                     console.log(res);
//                     if (res.status){
//                         // 关闭模态框
//                         $('#myModal1').modal('hide');
//                         window.location.reload();
//                     }else{
//                     // 显示错误信息
//                         $.each(res.error, function (name, error_list){
//                             $("#id_"+name).next().text(error_list[0])  // 循环输入
//                         })
//                 }
//                 }
//             })
//         })
//     }

function BtnDeleteEvent(){
    $('.btn-del').click(function (){
        $("#deleteModal").modal("show");
        DELETE_ID = $(this).attr("uid");
    })
}

function BtnDelInforEvent() {
    $('#ConfirmDelete').click(function (){
        $.ajax({
            url: '/admin/infor_del/',
            type: 'get',
            dataType: 'JSON',
            data: {
                'uid': DELETE_ID,
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


function BtnInfoInforEvent(){
    $('.btn-edit').click(function (){
        $('#myModalLabel').text("修改公告");
        $('#postData1').text("完成修改");
        var uid = $(this).attr("uid");
        EDIT_ID = uid;
        $.ajax({
            url: '/admin/infor_info/',
            type: 'get',
            dataType: 'JSON',
            data:{
                'infor_id': uid,
            },
            success: function (res){
                if(res.status){
                    // 将数据填充到模态框中
                    $.each(res.data, function (name, information){
                        $("#id_"+name).val(information);
                    })
                    // 显示模态框
                    $("#myModal1").modal('show');
                }else {
                    alert(res.result);
                }
            }
    })
    })

}

function BtnSaveInforEvent(){
    $('#postData1').click(function (){

        //清除所有的错误信息
        $(".error-msg").empty();
        // 判断EDIT_ID是否为空
        if(EDIT_ID){
            // 编辑
            Edit();
        }else {
            // 新建
            Add();
        }
    })
}
function Edit(){
     $.ajax({
            url: '/admin/infor_edit/' + "?infor_id=" + EDIT_ID,
            type: 'post',
            data: $('#PostForm1').serialize(),
            dataType: 'JSON',
            success: function (res){
                if(res.status) {
                    // alert("修改成功");
                    // 清空表单, PostForm是jQuery对象，("#PostForm")[0]是DOM元素
                    $("#PostForm1")[0].reset();
                    // 关闭模态框
                    $("#myModal1").modal('hide');
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

function Add(){
    $.ajax({
            url: '/admin/infor_save/',
            type: 'post',
            data: $('#PostForm1').serialize(),
            dataType: 'JSON',
            success: function (res){
                if(res.status) {
                    // alert("创建成功");
                    // 清空表单, PostForm是jQuery对象，("#PostForm")[0]是DOM元素
                    $("#PostForm1")[0].reset();
                    // 关闭模态框
                    $("#myModal1").modal('hide');
                    // 新增提示信息
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

function BtnShowInforEvent(){
    $('.btn-show').click(function (){
        var uid = $(this).attr("uid");
        // 请求数据
        $.ajax({
            url: '/admin/infor_info/',
            type: 'get',
            dataType: 'JSON',
            data:{
                'infor_id': uid,
            },
            success: function (res){
                if(res.status){
                    // 将数据填充到模态框中
                    // console.log(res.data.title);
                    $("#myShowModalLabel").text(res.data.title);
                    $("#myShowModalBody").text(res.data.context);
                    // 显示模态框，展示公告内容
                    $('#myShowModal').modal('show');
                }else {
                    alert(res.result);
                }
            }
    })

    })
}