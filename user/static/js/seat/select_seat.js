let FLOOR_ID;
$(function(){
    // $('#1th').show();


    bindFloorClickEvent();   // 动画的改变

    ShowSeat();              // 座位的展示
    bindClickPostEvent()     // 保存座位
    CancelEventModel();
    // seatManagerOrder();      // 处理管理员所预约的座位
    // setInterval(bindFloorClickEvent,5000);       // 页面定时刷新数据
})

function FirstDataGet() {
    var seatType = $('#seatType').text();
    $.ajax({
        url: "/getSeat/info/",
        type: "get",
        dataType: "JSON",
        data: {
            'seatType': seatType,
            'floor': FLOOR_ID,
        },
        success: function (res){
            for(let i = 0; i < res.result.length; i++){
                bindGenerateSeat(res.result[i]);     // 填写座位数据并生成座位
            }
        },
        error: function (){
            console.log('获取失败！！！');
        }
    })
}


function bindFloorClickEvent() {
    const floor = $(".floor");
    FLOOR_ID = 1;
    FirstDataGet();         // 页面最初时需要获取座位信息

    $('.floor').click(function (){
        FLOOR_ID = $(this).attr('uid');
        for (var i = 0; i<floor.length; i++){
            floor[i].classList.remove('active');
        }
        const floor_id = $(this).attr('id');
        this.classList.add('active');
        FirstDataGet();         // 获取数据
        // 更改页面
        $('.seatInfo').hide();

        $('.'+floor_id).show();
    })


}

function ShowSeat() {
    const seat = $(".seat");
    $('.seat').click(function (){
        for (var i = 0; i<seat.length; i++){
            seat[i].classList.remove('seat-click');
        }
        this.classList.add('seat-click');
        // 获取座位信息
        var seatId = $(this).attr('id');
        $('#seat-id').text(seatId);
        // // 将数据进行提交,将座位加锁
        // $.ajax({
        //     url: '/getSeat/lock/',
        //     type: 'post',
        //     dataType: 'JSON',
        //     data: {
        //         'seatId':seatId,
        //     },
        //     success: function (res){
        //         if(res.status){
        //             // 跳转页面
        //             console.log(res.result)
        //         }
        //     }
        // })
    })
}

function bindGenerateSeat(data) {
    // 填充数据
    var seatId = data['seatId']
    $('#'+seatId).text(data['seatId']);
    // 判断座位数据，进行渲染座位
    // console.log(data['seatPower']);
    if (data['seatPower'] === 1){
        $('#'+seatId).addClass('seat-power');
    }if(data['seatStatus'] === 2){
        $('#'+seatId).addClass('seat-order seat-disable');
    }if(data['seatStatus'] === 3){
        $('#'+seatId).addClass('seat-already seat-disable');
    }if(data['seatOrder'] === 1){                           // 需要满足管理员设置当前座位需要预约才能够进行选择
        // $('#'+seatId).addClass('seat-manager-order');
        // $('#'+seatId).addClass('seat-order seat-disable');
    }

}
function bindClickPostEvent(){
    // 用户确认后进行数据库的数据写入
    $('#seatPostData').click(function (){
        var seat_id = $('#seat-id').text();
        if(seat_id === ""){
            alert("请点击您想选择的座位!");
            window.location.reload();
        }else{
            // 进行提交数据保存
            $.ajax({
            url: '/getSeat/status_update/',
            type: 'post',
            dataType: 'JSON',
            data: {
                'seatId': seat_id,
                },
            success: function (res){
                if (res.status){
                    // 填充数据
                    $("#seat-order").attr('uid', res.seatId);
                    $('.seatId-order').text(res.seatId);
                    // $("#countdown").text(res.countdown);
                    $("#myModal").modal('show');
                }
            }
            })
        }
    })
}
function CancelEventModel(){
    $("#BtnConfirm").click(function (){
        $("#myModal").modal('hide');
        window.location.reload();
    })
}

function seatManagerOrder(){
    $(document).on('click', '.seat-manager-order', function(){
        $('#order-myModal').modal('show');
        
    })
    $('.btn-default').click(function(){
        var order_time_id = $(this).attr('id');
        var order_time = $('#'+order_time_id).text()
        $('.order-time').text(order_time);
    })
}
