import functools

def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            # Определяем способ логирования
            if filename:
                with open(filename, 'a') as f:
                    try:
                        f.write(f"{func.__name__} начало\n")
                        result = func(*args, **kwargs)
                        f.write(f"{func.__name__} ok\n")
                        return result
                    except Exception as e:
                        f.write(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}\n")
                        raise
            else:
                try:
                    print(f"{func.__name__} начало")
                    result = func(*args, **kwargs)
                    print(f"{func.__name__} ok")
                    return result
                except Exception as e:
                    print(f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}")
                    raise
        return wrapper
    return decorator