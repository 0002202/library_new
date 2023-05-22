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
    # orderTime_choices = (
    #     (1, '08:00~10:00'),
    #     (2, '10:00~12:00'),
    #     (3, '13:00~15:00'),
    #     (4, '15:00~17:00'),
    #     (5, '17:00~19:00'),
    #     (6, '19:00~21:00'),
    # )
    # # 只有用户选择了需要预约的座位时，才会存储预约时间
    # userOrderTime = models.CharField(verbose_name="预约时间", choices=orderTime_choices, max_length=64, default=None)
