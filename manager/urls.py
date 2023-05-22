"""专门用于配置管理员的URL"""

from django.urls import path
from manager.views import admin_login, admin_logout, admin_index, admin_seat, admin_information, admin_relationship, admin_black, \
    admin_seat_save, admin_seat_del, admin_seat_info, admin_seat_edit, admin_relationship_edit, admin_relationship_info,\
    admin_information_info, admin_information_save, admin_information_del, admin_information_edit, admin_black_save,\
    admin_black_info, admin_black_del, admin_black_update, admin_qr_code
urlpatterns = [
    # 将管理员所需要的页面进行展示
    path('login/', admin_login, name="show_admin_login"),
    path('logout/', admin_logout, name="show_admin_logout"),
    path('index/', admin_index, name="show_admin_index"),
    path('black/', admin_black, name="show_admin_black"),
    path('information/', admin_information, name="show_admin_information"),
    path('relationship/', admin_relationship, name="show_admin_relationship"),

    # 展示座位数据
    path('seat/', admin_seat, name="show_admin_seat"),
    path('seat_save/', admin_seat_save),
    path('seat_del/', admin_seat_del),
    path('seat_info/', admin_seat_info),
    path('seat_edit/', admin_seat_edit),

    # 展示预约关系相关数据
    path('user_info/', admin_relationship_info),
    path('user_edit/', admin_relationship_edit),

    # 展示系统公告的数据
    path('infor_info/', admin_information_info),
    path('infor_save/', admin_information_save),
    path('infor_edit/', admin_information_edit),
    path('infor_del/', admin_information_del),

    # 显示黑名单的数据
    path('black_save/', admin_black_save),
    path('black_info/', admin_black_info),
    path('black_update/', admin_black_update),
    path('black_del/', admin_black_del),

    # 展示二维码
    path('qr_code/', admin_qr_code, name="show_admin_qr_code"),

]
