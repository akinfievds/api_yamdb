from rest_framework.routers import DefaultRouter

from users.views import UserViewSet

router_v1 = DefaultRouter()

router_v1.register('v1/users', UserViewSet)


urlpatterns = []
urlpatterns += router_v1.urls
