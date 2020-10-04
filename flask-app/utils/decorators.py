from functools import wraps
from flask import request, redirect, url_for, abort

class AppDecorator:
    def content_type_check(f):
        @wraps(f)
        def decorated_function(*args, **kwargs):
            print('content-type', request.content_type)
            if request.content_type != "application/json":
                return redirect(url_for('error', next='/'))
            return f(*args, **kwargs)
        return decorated_function
    
    def limit_content_length(max_length):
        def decorator(f):
            @wraps(f)
            def wrapper(*args, **kwargs):
                cl = request.content_length
                if cl is not None and cl > max_length:
                    abort(413)
                return f(*args, **kwargs)
            return wrapper
        return decorator