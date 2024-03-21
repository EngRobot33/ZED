from utils.rate_limiter_handler import RateLimiterHandler

class RateLimiterMiddleware:

    def __init__(self,get_response) -> None:
        self.get_response = get_response

    def __call__(self,request) -> None:

        response = RateLimiterHandler.do_handler(request)

        if response is not None:
            return response

        return self.get_response(request)