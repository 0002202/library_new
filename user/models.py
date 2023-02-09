from django.db import models


class User(models.Model):
    userId = models.CharField(verbose_name="用户ID", max_length=255, blank=False, primary_key=True)
    userName = models.CharField(verbose_name="用户姓名", max_length=255, blank=False)
    userEmail = models.EmailField(verbose_name="用户邮箱", blank=False)
    userPassword = models.CharField(verbose_name="密码", max_length=255, blank=False)
    userIntegral = models.SmallIntegerField(verbose_name="信誉积分", default=3, blank=False)


class OnlineUser(models.Model):
    userId = models.CharField(verbose_name="登录用户ID", max_length=255, blank=False, primary_key=True)
    userSeat = models.CharField(verbose_name="座位ID", max_length=255, blank=True, default='未预约座位')
    userTime = models.DateTimeField(verbose_name="事件时间", blank=False)
    gender_choices = (
        (1, '未预约'),
        (2, '已预约'),
        (3, '已就坐'),
    )
    userStatus = models.SmallIntegerField(verbose_name="用户状态", choices=gender_choices, default=1)

