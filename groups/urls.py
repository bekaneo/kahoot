from rest_framework.routers import DefaultRouter

from groups.views import GroupViewSet

router = DefaultRouter()
router.register('', GroupViewSet)

urlpatterns = []

urlpatterns += router.urls
