$(function(){

    // bindBtnConfirmSeatEvent();  // 确认签到
    bindBtnCancelEvent();       // 取消预约
    count(timeIntDiff());                   //先执行一次这个函数  防止页面刷新出现空白
    CountDown();
    setInterval(() =>count(timeIntDiff()), 1000);       // 1秒钟调用一次的

    timeIntDiff();
});

function timeIntDiff(){
    var order_time = $('#countdown').text();
    // 必须满足这样的格式'2021/2/22 00:00:00'
    // console.log(order_time);
    return  order_time.substring(0, 4) +'/'+order_time.substring(5, 6)+'/'+order_time.substring(7, 8)+'/'+order_time.substring(10, 18) +':00';

}


function count(order_time) {
    var dateNow = +new Date(order_time);//当前时间的毫秒数
    var date2 = +new Date()//截止时间的毫秒数
    var cha = date2 - dateNow;//截止时间减去当前时间的毫秒
    // 计算天时分秒
    // let tian = parseInt(cha / (24 * 3600 * 1000)) //天数 1s = 1000ms
    var yu1 = cha % (24 * 3600 * 1000) //余数
    let hours = parseInt(yu1 / (3600 * 1000)) //小时
    var yu2 = yu1 % (3600 * 1000)
    let minutes = parseInt(yu2 / (60 * 1000)) //分钟
    var yu3 = yu2 % (60 * 1000);
    let seconds = parseInt(yu3 / 1000) //秒
    var maxtime = (30 - minutes) * 60 - seconds;        // 将相隔30分钟
    return maxtime;
}

function CountDown(maxtime=count(timeIntDiff())) {

        let msg;
        if (maxtime >= 0) {
            minutes = Math.floor(maxtime / 60);
            seconds = Math.floor(maxtime % 60);
            // msg = "距离签到结束还有" + minutes + "分" + seconds + "秒";
            // $('.time-item').text(msg);
            $('#seconds').text(seconds);
            $("#minutes").text(minutes);
            if (maxtime == 20 * 60) alert("还剩20分钟");
            --maxtime;
        } else {
            // 弹出模态框
            // alert("您已超时！！！");
            $('#myModal').modal('show');
            clearTimeout(t1);
            // 进行座位释放, 扣除信誉积分
            EventIntegralDispose()
            $("#BtnConfirm").click(function (){
                $('#myModal').modal('hide');
            })

        }
    }
    var t1 = setInterval("CountDown()", 1000);

function EventIntegralDispose() {
    var seatId = $(".seatId").text()
    // 向后端发起扣分请求
    $.ajax({
        url: '/deduct/',
        type: 'post',
        dataType: 'JSON',
        data: {
            'seatId': seatId,
        },
        success: function (res){
            if(res.status){
                // 跳转到主页
                $(window).attr('location','/');
            }else {
                alert(res.result);
            }
        }
    })
}

function bindBtnCancelEvent(){
    $('#seatCancelData').click(function (){
        var seatId = $('.seat-order').attr('id');
        $.ajax({
            url: '/getSeat/seat_cancel/',
            type: 'get',
            dataType: 'JSON',
            data:{
                'seatId': seatId,
            },
            success: function (res){
                if(res.status){
                    // 跳转页面
                    // $(window).attr('location','/select_seat/');
                    window.history.back();
                    console.log(res.result);
                }else{
                    alert(res.result);
                }
            }
        })
    })
}

function bindBtnConfirmSeatEvent() {
    $("#seatPostData").click(function (){
        var seatId = $('.seat-order').attr('id');
        $.ajax({
            url: '/getSeat/seat_save/',
            type: 'post',
            dataType: 'JSON',
            data: {
                'seatId': seatId,
            },
            success: function (res){
                if(res.status){
                    $(window).attr('location','/sign_success/');
                }else{
                    alert(res.result);
                }
            }
        })
    })
}