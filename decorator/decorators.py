import functools


def log(filename=None):
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            try:
                if filename:
                    with open(filename, "a") as f:
                        f.write(f"{func.__name__} начало\n")
                        result = func(*args, **kwargs)
                        f.write(f"{func.__name__} ok\n")
                        return result
                else:
                    print(f"{func.__name__} начало")
                    result = func(*args, **kwargs)
                    print(f"{func.__name__} ok")
                    return result
            except Exception as e:
                error_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                if filename:
                    with open(filename, "a") as f:
                        f.write(f"{error_message}\n")
                else:
                    print(error_message)
                raise

        return wrapper

    return decorator
