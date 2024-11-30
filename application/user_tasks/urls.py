from rest_framework.routers import SimpleRouter

from .views import UserTasksViewSet

app_name = 'user_tasks'

router = SimpleRouter()
router.register(r'tasks', UserTasksViewSet, basename='task')

urlpatterns = router.urls
