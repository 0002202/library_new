# Generated by Django 4.0.4 on 2023-02-01 07:30

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('manager', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='information',
            name='createName',
            field=models.CharField(default='admin', max_length=64, verbose_name='创建人'),
        ),
    ]
