from rest_framework import routers

from core.users.views import AuthorViewSet

router = routers.DefaultRouter()
router.register(r'', AuthorViewSet)
urlpatterns = router.urls
