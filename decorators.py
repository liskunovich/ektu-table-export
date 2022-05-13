import datetime


def timer(func):
    def inner(*args):
        start_time = datetime.datetime.now()
        result = func(*args)
        print(datetime.datetime.now() - start_time, func.__name__)
        return result
    return inner