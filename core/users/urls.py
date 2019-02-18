from rest_framework import routers

from core.users.views import *

router = routers.DefaultRouter()
router.register(r'', UserViewSet, basename='users')
urlpatterns = router.urls
