from django.urls import include, path
from rest_framework.routers import DefaultRouter

from users.views import TokenObtainView, UserViewSet, send_email

router_v1 = DefaultRouter()
router_v1.register('v1/users', UserViewSet)

urlpatterns = [
    path(
        'v1/auth/email/', send_email
    ),
    path(
        'v1/auth/token/',
        TokenObtainView.as_view(),
        name='token_obtain_pair'
    ),
    path('', include(router_v1.urls))
]
