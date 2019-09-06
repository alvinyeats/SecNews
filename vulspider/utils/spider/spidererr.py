
from django.core.mail import send_mail


class DownloadError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(str(self.value) + ": Download Page Failed!")


class ParseError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(str(self.value) + ": Download Page Failed!")


class CollectError(Exception):
    def __init__(self, value):
        self.value = value

    def __str__(self):
        return repr(str(self.value) + ": Download Page Failed!")


def spider_error(spider, err):
    err_msg = "Spider: " + spider + "\n" + err
    send_mail(
        "News Debug",
        err_msg,
        "admin@gmail.com",
        ["admin@gmail.com"],
        fail_silently=False,
    )
