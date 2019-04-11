#! _*_coding:utf-8 _*_
# __author__:"Irving"
from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from app01.forms.user import UserModelForm, UpdateUserModeForm, ResetPasswordUserModeForm
from rbac.service.urls import memory_reverse


def user_list(request):
    """
    用户列表
    :param request:
    :return:
    """
    users = models.UserInfo.objects.all()

    return render(request, "user_list.html", {'users': users})


def user_add(request):
    """
    添加用户
    :param request:
    :return:
    """
    if request.method == "GET":
        form = UserModelForm()
        return render(request, "rbac/change.html", {'form': form})

    form = UserModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))

    return render(request, "rbac/change.html", {'form': form})


def user_edit(request, pk):
    """
    编辑角色
    :param request:
    :param pk: 要修改角色的ID
    :return:
    """
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse("用户不存在")
    if request.method == "GET":
        form = UpdateUserModeForm(instance=obj)
        return render(request, "rbac/change.html", {'form': form})

    form = UpdateUserModeForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'user_list'))


def user_del(request, pk):
    """
    删除角色
    :param request:
    :param pk: 要删除角色的id
    :return:
    """
    origin_url = memory_reverse(request, 'user_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel_url': origin_url})

    models.UserInfo.objects.filter(id=pk).delete()

    return redirect(origin_url)


def user_reset_pwd(request, pk):
    """
    重置密码
    :param request:
    :param pk:
    :return:
    """
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse("用户不存在")
    if request.method == "GET":
        form = ResetPasswordUserModeForm()
        return render(request, "rbac/change.html", {'form': form})

    form = ResetPasswordUserModeForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'rbac:user_list'))

    return render(request, "rbac/change.html", {'form': form})
