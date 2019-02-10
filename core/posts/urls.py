from rest_framework import routers

from core.posts.views import PostsViewSet

router = routers.DefaultRouter()
router.register(r'', PostsViewSet)
urlpatterns = router.urls
