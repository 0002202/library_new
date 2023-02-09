"""
封装的分页组件
"""
from django.utils.safestring import mark_safe

"""
1、使用时可以设置分页大小，页面前后plus

2、在html前端需要加上：
    <nav aria-label="...">
        <ul class="pagination">
            {{ page_string }}<li><a>共：<b>{{ data_count }}</b>条</a></li>
        </ul>
    </nav>
"""


class Pagination(object):

    def __init__(self, request, queryset, page_param="page", page_size=6, plus=3):
        """

        :param request: 请求的对象
        :param queryset: 请求到的资源
        :param page_param: URL中携带的参数
        :param page_size: 页面显示数据条数，默认为6
        :param plus: 页面展示的前或后的页数，默认为3
        """
        import copy
        query_dict = copy.deepcopy(request.GET)
        query_dict._mutable = True
        self.query_dict = query_dict
        page = request.GET.get(page_param, '1')
        # 判断输入的参数是否为数字
        if page.isdecimal():
            page = int(page)
        else:
            page = 1

        data_count = queryset.count()  # 数据总数
        self.data_count = data_count
        """page_count为商，div为余数"""
        page_count, div = divmod(data_count, page_size)
        if div:
            page_count += 1  # 若余数不为0，则需要再加一页
        self.page = page
        self.page_param = page_param
        self.page_size = page_size
        self.start = (page - 1) * page_size
        self.end = page * page_size
        self.queryset = queryset[self.start: self.end]
        self.page_count = page_count    # 总页码
        self.plus = plus

    def html(self):
        # 计算出当前页的前3条和后3条
        if self.page_count <= 2 * self.plus + 1:
            start_page = 1
            end_page = self.page_count
        else:
            if self.page <= self.plus:
                start_page = 1
                end_page = 2 * self.plus + 1
            else:
                if (self.page + self.plus) > self.page_count:
                    start_page = self.page_count - 2 * self.plus
                    end_page = self.page_count
                else:
                    start_page = self.page - self.plus
                    end_page = self.page + self.plus
        page_list = []

        self.query_dict.setlist(self.page_param, [1])
        # 首页
        page_list.append('<li><a name="page" href="?{}">首页</a></li>'.format(self.query_dict.urlencode()))

        # 上一页
        if self.page > 1:
            self.query_dict.setlist(self.page_param, [self.page - 1])

            prev = '<li><a name="page" href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [1])
            prev = '<li><a name="page" href="?{}">上一页</a></li>'.format(self.query_dict.urlencode())
        page_list.append(prev)
        # 页面
        for i in range(start_page, end_page + 1):
            # 增加active类
            if i == self.page:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li name="page" class="active"><a href = "?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            else:
                self.query_dict.setlist(self.page_param, [i])
                ele = '<li name="page"><a href = "?{}">{}</a></li>'.format(self.query_dict.urlencode(), i)
            page_list.append(ele)
        # 下一页
        if self.page < self.page_count:
            self.query_dict.setlist(self.page_param, [self.page + 1])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        else:
            self.query_dict.setlist(self.page_param, [self.page_count])
            prev = '<li><a href="?{}">下一页</a></li>'.format(self.query_dict.urlencode())
        page_list.append(prev)
        # 尾页
        self.query_dict.setlist(self.page_param, [self.page_count])
        page_list.append('<li><a href="?{}">尾页</a></li>'.format(self.query_dict.urlencode()))
        page_string = mark_safe("".join(page_list))
        return page_string


