$(function (){
    // 导航条显示点击动画
    const nav = document.querySelector('#bs-example-navbar-collapse-1');
    const lis = nav.querySelectorAll('li');
    lis[1].classList.add('active');

    // 页面刷新后，应该查询空余座位
    // 向后端发送不同类型的座位页面
    // bindBtnSeatType();      //
})
// function bindBtnSeatType(){
//     $(".btn-primary").click(function (){
//         var seatType = $(this).attr('id');
//         $.ajax({
//             url: '/select_seat/',
//             type: 'get',
//             dataType: 'JSON',
//             data:{'seatType': seatType},
//             success: function (res){
//                 if(!res.status){
//                     alert(res.result);
//                 }
//             }
//         })
//     })
// }


