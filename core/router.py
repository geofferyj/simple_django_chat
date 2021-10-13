from django.conf import settings
from rest_framework.routers import DefaultRouter, SimpleRouter
from chat.views import RoomViewSet

from users.views import UserViewSet

if settings.DEBUG:
    router = DefaultRouter()
else:
    router = SimpleRouter()

router.register("users", UserViewSet)
router.register("rooms", RoomViewSet)

app_name = "api"
urlpatterns = router.urls