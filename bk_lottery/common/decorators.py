# coding=utf-8

"""
装饰器
1.权限pad装饰器，permission_required(已经写好装饰器，可自行定义验证逻辑)
"""

from django.http import HttpResponse
from django.utils.decorators import available_attrs
from django.shortcuts import redirect
from settings import SITE_URL
try:
    from functools import wraps
except ImportError:
    from django.utils.functional import wraps  # Python 2.4 fallback.


#===============================================================================
# 转义装饰器
#===============================================================================
def escape_exempt(view_func):
    """
            转义豁免，被此装饰器修饰的action可以不进行中间件escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_exempt = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)

def escape_script(view_func):
    """
            被此装饰器修饰的action会对GET与POST参数进行javascript escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_script = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)

def escape_url(view_func):
    """
            被此装饰器修饰的action会对GET与POST参数进行url escape
    """
    def wrapped_view(*args, **kwargs):
        return view_func(*args, **kwargs)
    wrapped_view.escape_url = True
    return wraps(view_func, assigned=available_attrs(view_func))(wrapped_view)


def _response_for_failure(request, _result, message, is_ajax):
    '''
            内部通用方法: 请求敏感权限出错时的处理(1和2)
    @param _result: 结果标志位
    @param message: 结果信息
    @param is_ajax: 是否是ajax请求
    '''
    if _result == 1:
        # 登陆失败，需要重新登录,跳转至登录页
        if is_ajax:
            return HttpResponse(status=402)
        return redirect(message)
    elif _result == 2:
        # error(包括exception)
        return _redirect_403(request)


def _redirect_403(request):
    '''转到403权限不足的提示页面'''
    url = SITE_URL + 'accounts/check_failed/?code=403'
    if request.is_ajax():
        resp = HttpResponse(status=403, content=url)
        return resp
    else:
        return redirect(url)

    
