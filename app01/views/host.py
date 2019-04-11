#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving

from django.shortcuts import render, redirect, HttpResponse
from app01 import models
from rbac.service.urls import memory_reverse
from app01.forms.host import HostModelForm


def host_list(request):
    """
    主机列表
    :param request:
    :return:
    """
    hosts = models.Host.objects.all()

    return render(request, "host_list.html", {'hosts': hosts})


def host_add(request):
    """
    添加主机
    :param request:
    :return:
    """
    if request.method == "GET":
        form = HostModelForm()
        return render(request, "rbac/change.html", {'form': form})

    form = HostModelForm(data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'host_list'))

    return render(request, "rbac/change.html", {'form': form})


def host_edit(request, pk):
    """
    编辑主机
    :param request:
    :param pk: 要修改主机的ID
    :return:
    """
    obj = models.UserInfo.objects.filter(pk=pk).first()
    if not obj:
        return HttpResponse("主机不存在")
    if request.method == "GET":
        form = HostModelForm(instance=obj)
        return render(request, "rbac/change.html", {'form': form})

    form = HostModelForm(instance=obj, data=request.POST)
    if form.is_valid():
        form.save()
        return redirect(memory_reverse(request, 'host_list'))


def host_del(request, pk):
    """
    删除主机
    :param request:
    :param pk: 要删除主机的id
    :return:
    """
    origin_url = memory_reverse(request, 'host_list')
    if request.method == 'GET':
        return render(request, 'rbac/delete.html', {'cancel_url': origin_url})

    models.Host.objects.filter(id=pk).delete()

    return redirect(origin_url)
