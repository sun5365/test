# -*- coding: utf-8 -*-
from django.http.response import HttpResponseForbidden, HttpResponseRedirect


class PermissionCheck(object):
    """
    禁止非管理员访问
    """

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        return response

    def process_view(self, request, view_func, view_args, view_kwargs):
        if "admin/login/" in request.path or "admin/logout/" in request.path:
            return None

        if not request.user.username:
            return HttpResponseRedirect('/admin/login/?next=%s' % request.path)

        if not request.user.is_superuser:
            return HttpResponseForbidden()
