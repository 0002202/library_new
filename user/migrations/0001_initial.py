# Generated by Django 4.1.2 on 2023-02-13 14:52

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='OnlineUser',
            fields=[
                ('userId', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='登录用户ID')),
                ('userSeat', models.CharField(blank=True, default='未预约座位', max_length=255, verbose_name='座位ID')),
                ('userTime', models.DateTimeField(verbose_name='事件时间')),
                ('userStatus', models.SmallIntegerField(choices=[(1, '未预约'), (2, '已预约'), (3, '已就坐')], default=1, verbose_name='用户状态')),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('userId', models.CharField(max_length=255, primary_key=True, serialize=False, verbose_name='用户ID')),
                ('userName', models.CharField(max_length=255, verbose_name='用户姓名')),
                ('userEmail', models.EmailField(max_length=254, verbose_name='用户邮箱')),
                ('userPassword', models.CharField(max_length=255, verbose_name='密码')),
                ('userIntegral', models.SmallIntegerField(default=3, verbose_name='信誉积分')),
            ],
        ),
    ]
