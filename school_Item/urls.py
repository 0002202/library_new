"""school_Item URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import manager
from django.urls import path, include
from user.views import show_index, show_seat, show_login, show_information, logout, select_seat, show_success

urlpatterns = [
    # path('manager/', manager.site.urls),
    path('', show_index, name="show_index"),
    path('show_seat/', show_seat, name="show_seat"),
    path('information/', show_information, name="show_information"),
    path('select_seat/', select_seat, name='select_seat'),
    path('login/', show_login, name="show_login"),
    path('logout/', logout, name="show_logout"),

    path("sign_success/", show_success),
    # 专用于座位数据查询
    path('getSeat/', include('seat.urls')),

    # 用于显示admin的url
    path('admin/', include('manager.urls'))

]
