#!/usr/bin/env python
# -*- coding:utf-8 -*-
# Author:Irving
import re
from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, render, redirect
from django.conf import settings


class Rbac(MiddlewareMixin):
    """
    用户URL进入URL路由控制器之前经过的中间件
    """

    def process_request(self, request):
        """
        1. 获取当前用户请求的URL
        2. 获取当前用户在session中保存的权限列表
        3. 权限信息匹配
        """

        current_url = request.path_info
        for valid_url in settings.VALID_URL_LIST:
            if re.match(valid_url, current_url):
                # 白名单中的URL无需权限验证即可访问
                return None

        permissions_dict = request.session.get(settings.PERMISSION_SESSION_KEY)

        if not permissions_dict:
            return HttpResponse("未获取到用户权限信息，请登录！")

        url_record = [
            {'title': '首页', 'url': '#'}
        ]

        # 此处代码进行判断
        for url in settings.NO_PERMISSION_LIST:
            if re.match(url, request.path_info):
                # 需要登录， 但无需权限校验
                request.current_selected_permission = 0
                request.breadcrumb = url_record
                return None

        flag = False

        for item in permissions_dict.values():
            reg = "^%s$" % item['url']
            if re.match(reg, current_url):
                flag = True
                request.current_selected_permission = item['pid'] or item['id']

                if not item['pid']:
                    url_record.extend([{'title': item['title'], 'url': item['url'], 'class': 'active'}])
                else:
                    url_record.extend([
                        {'title': item['p_title'], 'url': item['p_url']},
                        {'title': item['title'], 'url': item['url'], 'class': 'active'}
                    ])
                break

        request.breadcrumb = url_record

        if not flag:
            return HttpResponse("无权访问")
