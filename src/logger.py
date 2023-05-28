from datetime import datetime


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


def log(message: str):
    print(f"[{now()}] {message}")


def error(message: str):
    print(f"[{now()}] Error - {message}")
