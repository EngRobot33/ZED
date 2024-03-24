from django.contrib.auth.models import AnonymousUser

from channels.middleware import BaseMiddleware
from channels.db import database_sync_to_async

from rest_framework.authtoken.models import Token


class TokenAuthenticationMiddleWare(BaseMiddleware):

    async def __call__(self,scope,receive,send):

        try:
            token:str = scope.get("path").split("/")[-1] or scope.get("path").split("/")[-2]
        except:
            token = None

        scope["user"] = AnonymousUser()
        
        if token:
    
            user = await self.get_user_by_token(token)
            
            if user is not None:
                scope["user"] = user


        if not isinstance(scope["user"],AnonymousUser):
            return await super().__call__(scope,receive,send)
            
    @database_sync_to_async
    def get_user_by_token(self,token:str):

        token = Token.objects.filter(key = token).first()

        if token is not None:

            return token.user
        
        return None