from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from api.views import (CategoryViewSet, GenreViewSet, ReviewViewSet,
                       TitleViewSet)

router_v1 = DefaultRouter()
router_v1.register(
    'v1/genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'v1/categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'v1/titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'v1/titles',
    TitleViewSet,
    basename='titles'
)

urlpatterns = [
    path(
        'auth/token/',
        TokenObtainPairView.as_view(),
        name='token_obtain_pair'
    ),
    path(
        'auth/token/refresh/',
        TokenRefreshView.as_view(),
        name='token_refresh'
    ),
    path(
        '',
        include(router_v1.urls)
    )
]
