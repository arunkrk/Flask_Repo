from functools import wraps
from flask import g, request, redirect, url_for

class AppDecorator:
    def content_type_check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print('content-type', request.content_type)
            if request.content_type != "application/json":
                return redirect(url_for('error', next='/'))
            return f(*args, **kwargs)
        return decorated_function