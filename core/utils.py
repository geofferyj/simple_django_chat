from django.contrib.auth.models import AnonymousUser
from channels.db import database_sync_to_async
from django.db import close_old_connections
from rest_framework.authtoken.models import Token
from channels.middleware import BaseMiddleware
from channels.auth import AuthMiddlewareStack

from rest_framework.authentication import TokenAuthentication


@database_sync_to_async
def get_user(token_key):
    try:
        token = Token.objects.get(key=token_key)
        return token.user
    except Token.DoesNotExist:
        return AnonymousUser()
    finally:
        close_old_connections()

class TokenAuthMiddleware(BaseMiddleware):

    def __init__(self, inner):
        self.inner = inner

    async def __call__(self, scope, receive, send):
        token_key = scope['query_string'].decode().split('=')[-1]
        
        scope['user'] = await get_user(token_key)
        
        return await super().__call__(scope, receive, send)

TokenAuthMiddlewareStack = lambda inner: TokenAuthMiddleware(AuthMiddlewareStack(inner))


class QSTokenAuthentication(TokenAuthentication):
    """
    Extend the TokenAuthentication class to support querystring authentication
    in the form of "http://www.example.com/?auth_token=<token_key>"
    """
    def authenticate(self, request):
        # Check if 'token_auth' is in the request query params.
        # Give precedence to 'Authorization' header.
        if 'token' in request.query_params and \
                        'HTTP_AUTHORIZATION' not in request.META:
            return self.authenticate_credentials(request.query_params.get('token'))
        else:
            return super().authenticate(request)