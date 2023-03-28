from datetime import datetime


def now():
    return datetime.now().strftime('%Y:%m:%d %H:%M:%S')


def log(message):
    print(f'[{now()}] {message}')


def error(message):
    print(f'[{now()}] Error - {message}')
