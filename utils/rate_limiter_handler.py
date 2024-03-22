from typing import Optional,List

from datetime import datetime
from django.http.response import HttpResponse

from .redis_manager import RedisHandler

import json

redis_context = RedisHandler("localhost", 6379, 0)
redis_context.connect()


class RateLimiterHandler:
    USER_INFO_KEY: str = "user_{0}"
    USER_REQUEST_COUNT: str = "user_reqcount_{0}"
    USER_LAST_REQUEST_TIME: str = "user_lastreqtime_{0}"

    MESSAGE_TOO_MANY_REQUESTS: str = "you have sent too many requests , please try again in a minute later"

    redis_connection_error_counter: int = 0

    REQUEST_COUNT: int = 10
    EACH_SECONDS: int = 60

    @classmethod
    def do_handler(cls,request,allowed_paths:Optional[List[str]] = None) -> None | HttpResponse:

        if (allowed_paths is not None) and (request.path not in allowed_paths):
            return None

        client_ip: str = cls.__get_client_ip(request)
        try:
            ip = redis_context.redis_client.get(cls.USER_INFO_KEY.format(client_ip))

            if ip is not None:

                now = datetime.now()

                set_time: bytes = redis_context.redis_client.get(cls.USER_LAST_REQUEST_TIME.format(client_ip))
                set_time = set_time.decode()
                set_time = datetime.strptime(set_time, "%Y-%m-%d %H:%M:%S.%f")

                if cls.__check_time(now, set_time):
                    request_count: bytes = redis_context.redis_client.get(cls.USER_REQUEST_COUNT.format(client_ip))
                    request_count = int(request_count.decode())

                    if request_count > cls.REQUEST_COUNT:
                        content: str = json.dumps({"message": cls.MESSAGE_TOO_MANY_REQUESTS})
                        return HttpResponse(content=content, status=403)
                    redis_context.redis_client.incr(cls.USER_REQUEST_COUNT.format(client_ip))

                else:
                    redis_context.redis_client.delete(cls.USER_INFO_KEY.format(client_ip))
                    redis_context.redis_client.delete(cls.USER_REQUEST_COUNT.format(client_ip))
                    redis_context.redis_client.delete(cls.USER_LAST_REQUEST_TIME.format(client_ip))
            else:
                redis_context.redis_client.set(cls.USER_INFO_KEY.format(client_ip),client_ip)
                redis_context.redis_client.set(cls.USER_REQUEST_COUNT.format(client_ip),0)
                redis_context.redis_client.set(cls.USER_LAST_REQUEST_TIME.format(client_ip),str(datetime.now()))
        except ConnectionError:
            ...

    @classmethod
    def __check_time(cls, now: datetime, set_time: datetime) -> bool:
        return (now - set_time).seconds < cls.EACH_SECONDS

    @classmethod
    def __get_client_ip(cls, request) -> str:
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
