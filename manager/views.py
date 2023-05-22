import datetime

from django import forms
from django.http import JsonResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from user.utils.encrypt import md5
from manager.models import AdminUser, Information, BlackUser
from seat.models import Seat
from user.models import OnlineUser, User
from user.utils.Bootstrap import BootstrapModelForm

# Create your views here.
"""展示页面，管理员页面"""


class ManagerModelForm(BootstrapModelForm):
    class Meta:
        model = AdminUser
        fields = ['name', 'password']
        widgets = {
            'password': forms.PasswordInput,
        }

    # 钩子函数
    # 返回加密后的密码
    def clean_password(self):
        pwd = self.cleaned_data.get("password")
        return md5(pwd)


# 管理员登录
@csrf_exempt
def admin_login(request):
    if request.method == "GET":
        form = ManagerModelForm()
        return render(request, 'admin/login.html', {'form': form})  # 返回文本框
    form = ManagerModelForm(data=request.POST)
    if form.is_valid():
        # print(form.cleaned_data.get('password'))
        manager_data = AdminUser.objects.filter(name=form.cleaned_data.get('name'),
                                                password=form.cleaned_data.get('password')).first()  # 将所有的字段进行检查
        if not manager_data:
            form.add_error("password", "用户或密码错误")  # 主动添加错误信息
            return render(request, 'admin/login.html', {'form': form})
            # return JsonResponse({'status': False, 'result': '登录失败'})
        # 登录成功，新增session
        request.session['manager_name'] = {'id': manager_data.id, 'name': manager_data.name}
        return redirect('/admin/index')
    return render(request, 'admin/login.html', {'form': form})
    # return JsonResponse({'status': False, 'result': '数据验证失败'})


# 管理员登出
def admin_logout(request):
    request.session.flush()
    return redirect('/login/')


"""展示主页"""


def admin_index(request):
    if request.method == "GET":
        # 需要展示公告
        return render(request, 'admin/index.html')


"""展示座位"""


class SeatModelForm(BootstrapModelForm):
    # 定义一个用于创建座位的类
    class Meta:
        model = Seat
        fields = ['seatId', 'seatType', 'seatFloor', 'seatPower', 'seatCorridor', 'seatOrder']


def admin_seat(request):
    if request.method == "GET":
        searchSeatId = request.GET.get('searchSeatId', '')  # 需要所搜的座位编号
        data_dict = {}
        # 不为空，才会进行搜索
        if searchSeatId:
            data_dict['seatId__contains'] = searchSeatId
        form = SeatModelForm()  # 将创建新的元素

        # 处理页码
        from user.utils.pagination import Pagination
        queryset = Seat.objects.filter(**data_dict).order_by("seatId")
        page_object = Pagination(request, queryset)
        page_queryset = page_object.queryset  # 全部的数据
        data_count = page_object.data_count  # 总数据条数
        page_string = page_object.html()
        context = {
            "seat_info": page_queryset,
            "seat_add": form,
            "searchSeatId": searchSeatId,
            "page_string": page_string,
            "data_count": data_count
        }
        return render(request, 'admin/seat.html', context)


def admin_seat_save(request):
    """接收前端保存的座位数据"""
    form = SeatModelForm(data=request.POST)
    if form.is_valid():
        # 判断数据是否合法
        form.save()  # 存储到数据库中
        return JsonResponse({'status': True, 'result': '修改成功'})
    return JsonResponse({'status': False, 'error': form.errors})


def admin_seat_del(request):
    seatId = request.GET.get('seatId')
    print(seatId)
    exists = Seat.objects.filter(seatId=seatId).exists()
    if not exists:
        return JsonResponse({'status': False, 'result': '数据不存在，删除失败'})
    Seat.objects.filter(seatId=seatId).delete()  # 删除该座位数据
    return JsonResponse({'status': True, 'result': '删除成功!'})


def admin_seat_info(request):
    seatId = request.GET.get('seatId')
    print(seatId)
    row_seat_info = Seat.objects.filter(seatId=seatId).values('seatId', 'seatOrder', 'seatType', 'seatFloor',
                                                              'seatPower', 'seatCorridor').first()
    print(row_seat_info)
    if not row_seat_info:
        return JsonResponse({'status': False, 'result': '数据错误'})
    return JsonResponse({'status': True, 'data': row_seat_info})


def admin_seat_edit(request):
    """编辑座位"""
    seatId = request.GET.get("seatId")
    row_seat_info = Seat.objects.filter(seatId=seatId).first()
    if not row_seat_info:
        return JsonResponse({
            'status': False,
            'tips': '数据错误！',
        })
    # form = SeatModelForm(data=request.POST)
    # if form.is_valid():
    #     print(1)
    Seat.objects.filter(seatId=seatId).update(
        seatType=request.POST.get('seatType'),
        seatOrder=request.POST.get('seatOrder'),
        seatFloor=request.POST.get('seatFloor'),
        seatPower=request.POST.get('seatPower'),
        seatCorridor=request.POST.get('seatCorridor'),
    )
    return JsonResponse({'status': True, 'result': '修改成功'})
    # return JsonResponse({'status': False, 'error': form.errors})


"""展示预约关系"""


class onlineUserModelForm(BootstrapModelForm):
    class Meta:
        model = OnlineUser
        fields = '__all__'


def admin_relationship(request):
    if request.method == "GET":
        searchUserId = request.GET.get('searchUserId', '')  # 需要所搜的座位编号
        data_dict = {}
        # 不为空，才会进行搜索
        if searchUserId:
            data_dict['userId__contains'] = searchUserId
        from user.utils.pagination import Pagination
        queryset = OnlineUser.objects.filter(**data_dict).order_by("userId")
        page_object = Pagination(request, queryset)
        page_queryset = page_object.queryset  # 全部的数据
        data_count = page_object.data_count  # 总数据条数
        page_string = page_object.html()
        form = onlineUserModelForm()
        # print(page_queryset.values()[0].get(''))
        return render(request, 'admin/relationship.html', {
            'userData': page_queryset,
            "user_info_add": form,
            'data_count': data_count,
            'page_string': page_string,
            'searchUserId': searchUserId,

        })


def admin_relationship_info(request):
    userId = request.GET.get('userId')
    row_user_info = OnlineUser.objects.filter(userId=userId).values('userId', 'userSeat', 'userTime',
                                                                    'userStatus').first()
    if not row_user_info:
        return JsonResponse({'status': False, 'result': '数据错误'})
    return JsonResponse({'status': True, 'data': row_user_info})


def admin_relationship_edit(request):
    """编辑预约信息"""
    # 将当前时间存储到表中
    now_time = datetime.datetime.now()
    userId = request.GET.get("userId")
    row_user_info = OnlineUser.objects.filter(userId=userId).first()
    if not row_user_info:
        return JsonResponse({
            'status': False,
            'tips': '数据错误！',
        })
    OnlineUser.objects.filter(userId=userId).update(
        userSeat=request.POST.get('userSeat'),
        userTime=now_time,
        userStatus=request.POST.get('userStatus'),
    )
    return JsonResponse({'status': True, 'result': '修改成功'})


"""展示公告"""


class informationModelForm(BootstrapModelForm):
    class Meta:
        model = Information
        fields = ['title', 'context', 'file']


def admin_information(request):
    if request.method == "GET":
        searchInforId = request.GET.get('searchInforId', '')  # 需要所搜的座位编号
        data_dict = {}
        # 不为空，才会进行搜索
        if searchInforId:
            data_dict['id__contains'] = searchInforId
        form = informationModelForm()  # 将创建新的元素

        # 处理页码
        from user.utils.pagination import Pagination
        queryset = Information.objects.filter(**data_dict).order_by('createTime')
        page_object = Pagination(request, queryset)
        page_queryset = page_object.queryset  # 全部的数据
        data_count = page_object.data_count  # 总数据条数
        page_string = page_object.html()
        context = {
            "information_info": page_queryset,
            "infor_add": form,
            "searchInforId": searchInforId,
            "page_string": page_string,
            "data_count": data_count
        }
        return render(request, 'admin/information.html', context)


def admin_information_save(request):
    # 将前端提交的数据进行校验和过滤
    if request.method == 'POST':
        # 将数据提交到数据库
        form = informationModelForm(data=request.POST)
        # 校验数据
        if form.is_valid():
            # 存入数据
            now_datetime = datetime.datetime.now()
            # form.cleaned_data['createTime'] = now_datetime    # 往数据字典中加入时间
            print(form.cleaned_data)
            Information(
                title=form.cleaned_data.get('title'),
                context=form.cleaned_data.get('context'),
                file=form.cleaned_data.get('file'),
                createTime=now_datetime
            ).save()  # 保存时间
            # up_file = request.FILES.get('upload_file')
            # Information(path=up_file).save()

            return JsonResponse({'status': True, 'result': '修改成功'})
        return JsonResponse({'status': False, 'error': form.errors})
        # return HttpResponse("hh")


def admin_information_del(request):
    # 获取到前端返回的公告Id后，进行删除
    infor_id = request.GET.get('uid')
    print(infor_id)
    exists = Information.objects.filter(id=infor_id).exists()
    if not exists:
        return JsonResponse({'status': False, 'result': '数据不存在，删除失败'})
    Information.objects.filter(id=infor_id).delete()  # 删除该座位数据
    return JsonResponse({'status': True, 'result': '删除成功!'})


def admin_information_edit(request):
    infor_id = request.GET.get("infor_id")
    row_infor_info = Information.objects.filter(id=infor_id).first()
    if not row_infor_info:
        return JsonResponse({
            'status': False,
            'tips': '数据错误！',
        })
    form = informationModelForm(data=request.POST)
    if form.is_valid():
        print("验证成功")
        now_datetime = datetime.datetime.now()
        # file = request.POST.get('file')
        # print(file)
        # if not file:
        #     file = None
        Information.objects.filter(id=infor_id).update(
            title=request.POST.get('title'),
            context=request.POST.get('context'),
            # file=file,
            createTime=now_datetime,
        )
        return JsonResponse({'status': True, 'result': '修改成功'})


def admin_information_info(request):
    # 展示系统公告信息
    infor_id = request.GET.get('infor_id')
    print(infor_id)
    row_infor_info = Information.objects.filter(id=infor_id).values('title', 'createName', 'createTime',
                                                                    'context').first()
    print(row_infor_info)
    if not row_infor_info:
        return JsonResponse({'status': False, 'result': '数据错误'})
    return JsonResponse({'status': True, 'data': row_infor_info})


"""处理用户黑名单"""


class BlackUserModelForm(BootstrapModelForm):
    class Meta:
        model = BlackUser
        fields = ['userId', 'blackCause', 'cancelTime']


# 专用于更新处理
class BlackUserUpdateModelForm(BootstrapModelForm):
    class Meta:
        model = BlackUser
        fields = ['cancelTime']


def admin_black(request):
    if request.method == "GET":
        searchUserId = request.GET.get('searchUserId', '')  # 需要所搜的座位编号
        data_dict = {}
        # 不为空，才会进行搜索
        if searchUserId:
            data_dict['userId__contains'] = searchUserId
        form = BlackUserModelForm()
        form_update = BlackUserUpdateModelForm()
        # 处理页码
        from user.utils.pagination import Pagination
        queryset = BlackUser.objects.filter(**data_dict).order_by('createTime')
        page_object = Pagination(request, queryset)
        page_queryset = page_object.queryset  # 全部的数据
        data_count = page_object.data_count  # 总数据条数
        page_string = page_object.html()
        context = {
            "black_user": page_queryset,
            "add_info": form,
            "add_info_update": form_update,
            "searchUserId": searchUserId,
            "page_string": page_string,
            "data_count": data_count
        }
        return render(request, 'admin/black.html', context)


def admin_black_save(request):
    form = BlackUserModelForm(data=request.POST)
    if form.is_valid():
        # 判断数据是否合法
        now_datetime = datetime.datetime.now()
        userId = form.cleaned_data.get('userId')
        # 需要校验改用户是否注册
        userId_is = User.objects.filter(userId=userId).first()
        if not userId_is:
            return JsonResponse({'status': False, 'userError': '用户编号有误！'})
        cancelTime = form.cleaned_data.get('cancelTime')
        # 需要校验失效时间是否比创建时间小
        if cancelTime < now_datetime:
            return JsonResponse({'status': False, 'timeError': '解除时间不能小于当前时间'})
        # print(form.cleaned_data)
        BlackUser(
            userId=form.cleaned_data.get('userId'),
            blackCause=form.cleaned_data.get('blackCause'),
            cancelTime=form.cleaned_data.get('cancelTime'),
            createTime=now_datetime
        ).save()
        return JsonResponse({'status': True, 'result': '修改成功'})
    return JsonResponse({'status': False, 'error': form.errors})


def admin_black_info(request):
    userId = request.GET.get('blackUserId')
    # 进行查找数据
    createTime = BlackUser.objects.filter(userId=userId).values('createTime')[0].get('createTime')
    cancelTime = BlackUser.objects.filter(userId=userId).values('cancelTime')[0].get('cancelTime')
    return JsonResponse({'status': True, 'createTime': createTime, 'cancelTime': cancelTime})


def admin_black_update(request):
    userId = request.GET.get("BlackUserId")
    print(userId)
    row_black_info = BlackUser.objects.filter(userId=userId).first()
    if not row_black_info:
        return JsonResponse({
            'status': False,
            'tips': '数据错误！',
        })
    form = BlackUserUpdateModelForm(data=request.POST)
    if form.is_valid():
        print(form.cleaned_data)
        # 判断时间是否小于创建时间
        cancelTime = form.cleaned_data.get('cancelTime')
        createTime = BlackUser.objects.filter(userId=userId).values('createTime')[0].get('createTime')
        if cancelTime < createTime:
            return JsonResponse({'status': False, 'timeError': '解除时间不能小于当前时间'})

        BlackUser.objects.filter(userId=userId).update(cancelTime=cancelTime)
        return JsonResponse({'status': True, 'result': '修改成功'})
    return JsonResponse({'status': False, 'result': '修改失败'})


def admin_black_del(request):
    userId = request.GET.get('blackUserId')
    exists = BlackUser.objects.filter(userId=userId).exists()
    if not exists:
        return JsonResponse({'status': False, 'result': '数据不存在，删除失败'})
    BlackUser.objects.filter(userId=userId).delete()  # 删除该座位数据
    return JsonResponse({'status': True, 'result': '删除成功!'})


# 展示二维码
def admin_qr_code(request):
    return render(request, 'admin/Qrcode.html')