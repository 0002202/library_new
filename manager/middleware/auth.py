from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import redirect


class ManagerLogin(MiddlewareMixin):
    """检查管理员携带的session，定义中间价"""

    def process_request(self, request):
        """定义一个不需要检查session的URL列表"""
        NotCheckUrl = ['/admin/login/', '/login/', '/show_seat/', '/information/', '/', '/logout/']

        # 排除不需要验证的页面，当获取到用户请求的URL为/admin/login/时，则允许通过
        # if request.path_info == '/admin/login/' or request.path_info == '/login/' or request.path_info == '/login/':
        if request.path_info in NotCheckUrl:
            return
        # 获取session信息，进行放行页面
        manager_info = request.session.get('manager_name')
        user_info = request.session.get('user_name')
        if user_info and not manager_info:
            UserCheckUrl = ['/', '/select_seat/', '/getSeat/info/', '/getSeat/lock/', '/getSeat/status_update/',
                            '/getSeat/seat_cancel/', '/getSeat/seat_save/', '/getSeat/leave/', '/sign_success/']
            if request.path_info in UserCheckUrl:
                return
        if not user_info and manager_info:
            ManagerCheckUrl = ['/admin/index/', '/admin/black/', '/admin/information/', '/admin/relationship/',
                               '/admin/seat/']
            if request.path_info in ManagerCheckUrl:
                return
        else:
            return redirect('/login/')



