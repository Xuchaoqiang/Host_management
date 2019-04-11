#! _*_coding:utf-8 _*_
# __author__:"Irving"
from django.shortcuts import render


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """

    return render(request, "user_list.html")
