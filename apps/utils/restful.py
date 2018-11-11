from django.http import JsonResponse

class HttpCode(object):
    ok = 200
    noauth = 401
    params_error = 400
    method_error = 405
    server_error = 500

def result(code=HttpCode.ok,message="",data=None,kwargs=None):
    json_dict = {'code':code,"msg":message,'data':data}
    if kwargs and isinstance(kwargs,dict) and kwargs.keys():
        json_dict.update(kwargs)
    return JsonResponse(json_dict)

def ok():
    return result()

def noauth(message='没有权限'):
    return result(code=HttpCode.noauth,message=message)

def params_error(message='参数错误'):
    return result(code=HttpCode.params_error,message=message)

def method_error(message='参数错误'):
    return result(code=HttpCode.method_error,message=message)

def server_error(message='服务器内部错误'):
    return result(code=HttpCode.server_error,message=message)