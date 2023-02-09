from django.db import models


# Create your models here.


class AdminUser(models.Model):
    id = models.IntegerField(verbose_name="编号", blank=False, primary_key=True)
    name = models.CharField(verbose_name="用户名", max_length=32, blank=False)
    password = models.CharField(verbose_name="用户密码", max_length=64, blank=False)

    def __str__(self):
        return self.name


class Information(models.Model):
    id = models.AutoField(verbose_name="公告编号", blank=False, primary_key=True)  # 系统默认创建的
    title = models.CharField(verbose_name="公告标题", max_length=255, blank=False)
    context = models.TextField(verbose_name="公告内容", blank=False)
    file = models.FileField(verbose_name="公告附件", blank=True, upload_to='files/')
    createTime = models.DateTimeField(verbose_name="创建时间", blank=False)
    # updateTime = models.DateTimeField(verbose_name="更新时间", blank=False)

    # 创建人
    createName = models.CharField(verbose_name="创建人", max_length=64, default="admin")


class BlackUser(models.Model):
    userId = models.CharField(verbose_name="用户编号", max_length=255, blank=False, primary_key=True)
    createTime = models.DateTimeField(verbose_name="创建时间", blank=False)
    cancelTime = models.DateTimeField(verbose_name="解除时间", blank=False)
    blackCause = models.TextField(verbose_name="公告内容", blank=False, default="系统拉黑")
