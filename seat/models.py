from django.db import models

from user.models import OnlineUser
"""创建座位模型，主要负责生成座位数据"""


class Seat(models.Model):
    seatId = models.CharField(verbose_name="座位ID", max_length=255, blank=False, primary_key=True)
    seat_type = (
        (1, '自习区'),
        (2, '阅读区'),
        (3, '休闲区'),
    )
    seatType = models.SmallIntegerField(verbose_name="座位类型", blank=False, choices=seat_type, default=1)
    seat_Floor = (
        (1, '一楼'),
        (2, '二楼'),
        (3, '三楼'),
        (4, '四楼'),
        (5, '五楼'),
    )
    seatFloor = models.SmallIntegerField(verbose_name="所在楼层", blank=False, choices=seat_Floor, default=1)
    seat_status = (
        (1, '未预约'),
        (2, '已预约'),
        (3, '已就坐'),
    )
    seatStatus = models.SmallIntegerField(verbose_name="座位状态", choices=seat_status, default=1)
    # 外键seatStatus，关联表onlineUser，座位状态改变则改变
    seatInfo_choices = (
        (1, '是'),
        (2, '否'),
    )
    seatPower = models.SmallIntegerField(verbose_name="拥有电源", choices=seatInfo_choices, default=2)
    seatCorridor = models.SmallIntegerField(verbose_name="靠近走廊", choices=seatInfo_choices, default=2)
    seatOrder = models.SmallIntegerField(verbose_name="需要预约", choices=seatInfo_choices, default=2)


