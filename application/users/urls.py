from rest_framework.routers import SimpleRouter

from .views import UserViewSet, TokenViewSet

app_name = 'users'

router = SimpleRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'tokens', TokenViewSet, basename='token')

urlpatterns = router.urls
