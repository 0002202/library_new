import datetime
from django import forms
from django.http import JsonResponse, HttpResponse
from django.core.exceptions import ValidationError
from django.shortcuts import render, redirect
from seat.models import Seat
from user.models import User, OnlineUser
from manager.models import Information

from user.utils.Bootstrap import BootstrapModelForm

# Create your views here.
from user.utils.encrypt import md5

"""展示页面，学生用户"""


def show_index(request):
    if request.method == 'GET':
        try:
            user_seatId = request.session.get('user_seat').get('seatId')
            user_is_already = request.session.get('user_already').get('is_already')
        except:
            user_is_already = None
        if user_is_already:
            userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
                get('userName')
            title = '注销'
            countdown = OnlineUser.objects.filter(userSeat=user_seatId).values('userTime')[0].get('userTime')
            return render(request, 'user/sign_success.html', {
                'countdown': countdown,
                'userName': userName,
                'title': title
            })
        data = {}
        queryData = Information.objects.filter().order_by("-createTime")
        try:
            userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
                get('userName')
            data['userName'] = userName
            data['title'] = '注销'
            data['queryData'] = queryData
            return render(request, 'user/index.html', data)
        except AttributeError:
            data['userName'] = '登录'
            data['title'] = '登录'
            data['queryData'] = queryData
            return render(request, 'user/index.html', data)


# 展示页面的同时需要展示空座数量
def show_seat(request):
    if request.method == 'GET':
        # 返回座位数量
        """seatStatus：1,2,3分别是未预约、已预约、已就坐"""
        """seatType：1,2,3分别是自习区、阅读区、休闲区"""
        study = Seat.objects.filter(seatType='1', seatStatus='1').count()
        standard = Seat.objects.filter(seatType='2', seatStatus='1').count()
        leisure = Seat.objects.filter(seatType='3', seatStatus='1').count()
        try:
            userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
                get('userName')
            title = '注销'
        except AttributeError:
            userName = '登录'
            title = '登录'
        data = {'studySeatNumber': study,
                'leisureSeatNumber': leisure,
                'standardSeatNumber': standard,
                'userName': userName,
                'title': title}
        return render(request, 'user/seat.html', data)


# 进行选择座位
def select_seat(request):
    if request.method == 'GET':
        try:
            userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
                get('userName')
            title = '注销'
        except AttributeError:
            userName = '登录'
            title = '登录'
        seatType = ['自习区', '阅读区', '休闲区']
        try:
            # 判断用户是否已经预约座位，若用户已经预约则不对用户显示选作页面，显示签到页面
            user_is_order = request.session.get('user_seat').get('is_order')
            user_seatId = request.session.get('user_seat').get('seatId')
            try:
                user_is_already = request.session.get('user_already').get('is_already')
            except:
                user_is_already = None
            user_userTime = OnlineUser.objects.filter(userSeat=user_seatId).values('userTime')[0].get('userTime')
            if user_is_order and not user_is_already:
                # 返回签到页面
                return render(request, 'user/sign_in.html', {
                    'countdown': user_userTime,
                    'seatId': user_seatId,
                    'userName': userName,
                    'title': title,
                })
            elif user_is_order and user_is_already:
                countdown = OnlineUser.objects.filter(userSeat=user_seatId).values('userTime')[0].get('userTime')
                return render(request, 'user/sign_success.html', {
                    'countdown': countdown,
                    'userName': userName,
                    'title': title
                })
        except:
            return render(request, 'seat/select_seat.html', {
                'seatType': seatType,
                'userName': userName,
                'title': title,
            })


# 显示系统公告
def show_information(request):
    # 判断是否携带用户session，如果携带则展示个人信息和馆内通知
    print(request.session.get('user_name'))
    if request.method == 'GET':
        try:
            userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
                get('userName')
            title = '注销'
        except AttributeError:
            userName = '登录'
            title = '登录'
        return render(request, 'user/information.html', {
            'userName': userName,
            'title': title,
        })


class UserLogUp(BootstrapModelForm):
    confirm_password = forms.CharField(label="确认密码", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['userId', 'userName', 'userEmail', 'userPassword', 'confirm_password']
        widgets = {
            'userPassword': forms.PasswordInput(render_value=True),  # 改为密码框
        }

    def clean_userPassword(self):
        pwd = self.cleaned_data.get('userPassword')
        return md5(pwd)

    def clean_confirm_password(self):
        pwd = self.cleaned_data.get('userPassword')
        confirm = md5(self.cleaned_data.get('confirm_password'))
        if pwd != confirm:
            raise ValidationError("两次密码不一致")
        else:
            return confirm

    def clean_userId(self):
        userId = self.cleaned_data.get('userId')
        data = User.objects.filter(userId=userId).first()
        if data:
            raise ValidationError("该账号已注册！")
        else:
            return userId


class UserLogIn(BootstrapModelForm):
    # 因为创建的框的id重复，所以新创建两个新的Input框
    login_userId = forms.CharField(label="用户账号", widget=forms.TextInput)
    login_userPassword = forms.CharField(label="用户密码", widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = []
        widgets = {
            'login_userPassword': forms.PasswordInput(),  # 改为密码框
        }

    def clean_login_userPassword(self):
        pwd = self.cleaned_data.get('login_userPassword')
        return md5(pwd)


# 用户登录
def show_login(request):
    if request.method == 'GET':
        formLogUp = UserLogUp()
        formLogIn = UserLogIn()
        return render(request, 'login/login.html',
                      {
                          'formLogUp': formLogUp,
                          'formLogIn': formLogIn,
                      })
    formLogUp = UserLogUp(data=request.POST)
    formLogIn = UserLogIn(data=request.POST)
    if formLogUp.is_valid():
        formLogUp.save()

        return render(request, 'login/login.html',
                      {
                          'class': 'right-panel-active',
                          'msg': "注册成功，请登录"
                      })
    if formLogIn.is_valid():
        # 判断用户账号域密码是否正确
        status = User.objects.filter(
            userId=formLogIn.cleaned_data.get('login_userId'),
            userPassword=formLogIn.cleaned_data.get('login_userPassword'),
        ).first()
        if status:
            # 登录成功
            # 记录session
            request.session['user_name'] = {
                'userId': formLogIn.cleaned_data.get('login_userId'),
                'is_login': True
            }
            # 还需要将用户记录到在线用户表中
            nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            data = OnlineUser(userId=formLogIn.cleaned_data.get('login_userId'), userTime=nowTime)
            data.save()
            userName = User.objects.filter(userId=formLogIn.cleaned_data.get('login_userId')).values('userName')[0]. \
                get('userName')
            queryData = Information.objects.filter().order_by("-createTime")
            return render(request, 'user/index.html',
                          {
                              'userName': userName, 'title': '注销',
                              'queryData': queryData,
                          })
        return render(request, 'login/login.html',
                      {
                          'formLogIn': formLogIn,
                      })
    # 显示错误信息
    return render(request, 'login/login.html',
                  {
                      'formLogUp': formLogUp,
                      'formLogIn': formLogIn,
                  })


# 用户签到成功后，即展示签到成功页面
def show_success(request):
    if request.session.get('user_seat').get('is_order'):
        userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
            get('userName')
        title = '注销'
        userId = request.session.get('user_name').get('userId')
        countdown = OnlineUser.objects.filter(userId=userId).values('userTime')[0].get('userTime')
        # 才会显示签到成功页面
        return render(request, 'user/sign_success.html', {
            'countdown': countdown,
            'userName': userName,
            'title': title
        })
    else:
        return HttpResponse("数据错误！！！")


# 用户正常离馆
def leave(request):
    if request.method == 'GET':
        userId = request.session.get('user_name').get('userId')
        seatId = OnlineUser.objects.filter(userId=userId).values('userSeat')[0].get('userSeat')
        nowTime = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        # 释放座位，修改座位状态
        Seat.objects.filter(seatId=seatId).update(seatStatus=1)
        OnlineUser.objects.filter(userId=userId).update(userStatus=1, userTime=nowTime, userSeat="未预约座位")
        request.session['user_seat'] = {
            'seatId': None,
            'is_order': False
        }
        userName = User.objects.filter(userId=request.session.get('user_name').get('userId')).values('userName')[0]. \
            get('userName')
        title = '注销'
        queryData = Information.objects.filter().order_by("-createTime")
        return render(request, 'user/index.html', {
            'userId': userId,
            'seatId': seatId,
            'queryData': queryData,
            'userName': userName,
            'title': title
        })


# 用户注销
def logout(request):
    if request.method == 'GET':
        # 删除onlineUser表中的数据
        try:
            OnlineUser.objects.filter(userId=request.session.get('user_name').get('userId')).first().delete()
        # request.session.clear()
        except AttributeError:
            pass
        request.session.flush()
        return redirect('/login')
