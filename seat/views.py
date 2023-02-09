import datetime
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt

from user.models import OnlineUser, User
from seat.models import Seat


# Create your views here.


def seat_info(request):
    seatType = request.GET.get('seatType')
    seatFloor = request.GET.get('floor')
    if '自习室' in seatType:
        seatType_num = 1
    elif '阅读区' in seatType:
        seatType_num = 2
    else:
        seatType_num = 3
    seatData = Seat.objects.filter(seatType=seatType_num, seatFloor=seatFloor).all().values()
    singleSeatData = []
    singleSeatId, singleSeatPower, singleSeatFloor, singleSeatOrder, singleSeatStatus, singleSeatCorridor = [], [], [], [], [], []
    for i in seatData:
        singleSeatData.append(i)
        singleSeatId.append(i.get('seatId'))
        singleSeatPower.append(i.get('seatPower'))
        singleSeatFloor.append(i.get('seatFloor'))
        singleSeatOrder.append(i.get('seatOrder'))
        singleSeatStatus.append(i.get('seatStatus'))
        singleSeatCorridor.append(i.get('seatCorridor'))
    # print(singleSeatId, singleSeatStatus, singleSeatPower, singleSeatFloor, singleSeatOrder)
    data = {
        'status': True,
        'result': singleSeatData,  # 将一楼的座位数据传给前端
    }
    return JsonResponse(data)


@csrf_exempt
def seat_lock(request):
    """给座位加锁"""
    seatId = request.POST.get('seatId')
    # 将传入的座位编号进行锁定
    return JsonResponse({
        'status': True,
        'result': '获取成功'
    })


@csrf_exempt
def seat_status_update(request):
    """座位状态更新"""
    seatId = request.POST.get('seatId')
    table_seatStatus = Seat.objects.filter(seatId=seatId).values('seatStatus')[0].get('seatStatus')
    if table_seatStatus == 1:
        # 获取用户数据
        loginUserId = request.session.get('user_name').get('userId')
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')

        # 修改数据库中信息
        Seat.objects.filter(seatId=seatId).update(seatStatus=2)  # 座位状态改为被预约,2为被预约，并将数据更新
        OnlineUser.objects.filter(userId=loginUserId).update(userSeat=seatId, userTime=nowTime, userStatus=2)

        # 记录用户session，防止用户再次选择
        request.session['user_seat'] = {
            'seatId': seatId,
            'is_order': True
        }
        return JsonResponse({
            'status': True,
            'countdown': nowTime,
            'seatId': seatId,
        })
    else:
        return redirect(request, '/getSeat/select_seat/')


def seat_cancel(request):
    """处理用户取消签到"""
    seatId = request.GET.get('seatId')
    # print(seatId)
    user_object = OnlineUser.objects.filter(userSeat=seatId).first()
    if not user_object:
        # 表示该座位未被预约，返回报错信息
        return JsonResponse({
            'status': False,
            'result': '取消失败，该座位未被预约'
        })
    # 更改数据
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    OnlineUser.objects.filter(userSeat=seatId).update(userSeat="未预约座位", userStatus=1, userTime=nowTime)
    Seat.objects.filter(seatId=seatId).update(seatStatus=1)
    request.session['user_seat'] = {
        'seatId': None,
        'is_order': False
    }
    return JsonResponse({
        'status': True,
        'result': '取消成功！'
    })


def seat_save(request):
    """确认签到"""
    seatId = request.GET.get('seatId')
    # print(seatId)
    user_object = OnlineUser.objects.filter(userSeat=seatId).first()
    if not user_object:
        # 表示该座位未被预约，返回报错信息
        return JsonResponse({
            'status': False,
            'result': '签到失败，该座位未被预约'
        })
    nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    OnlineUser.objects.filter(userSeat=seatId).update(userStatus=3, userTime=nowTime)
    Seat.objects.filter(seatId=seatId).update(seatStatus=3)
    return JsonResponse({
        'status': True,
        'result': '签到成功！'
    })
