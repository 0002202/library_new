# Generated by Django 4.0.4 on 2023-02-09 12:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='onlineuser',
            name='userSeat',
            field=models.CharField(blank=True, default='未预约座位', max_length=255, verbose_name='座位ID'),
        ),
    ]
