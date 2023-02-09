$(function (){
    setInterval(() =>count(timeIntDiff()), 1000);
    timeIntDiff();
    leaveLibrary();     // 用户离馆
})

function timeIntDiff(){
    var order_time = $('#countdown').text();
    // 必须满足这样的格式'2021/2/22 00:00:00'
    return  order_time.substring(0, 4) +'/'+order_time.substring(5, 6)+'/'+order_time.substring(7, 8)+'/'+order_time.substring(10, 15) +':00';
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
    $('#hour_show').text(hours);
    $('#minute_show').text(minutes);
    $("#second_show").text(seconds);
}

function leaveLibrary(){
    $("#leaveLibrary").click(function (){
        $("#leaveModal").modal('show');
        $('#ConfirmLeave').click(function (){
            $("#leaveModal").modal('hide');
            $(window).attr('location','/getSeat/leave/');
        })
    })
}