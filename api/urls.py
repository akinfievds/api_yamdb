from django.urls import include, path
from rest_framework.routers import DefaultRouter

from api.views import (
    CategoryViewSet, CommentsViewSet, GenreViewSet, ReviewViewSet,
    TitleViewSet, UserViewSet
)
from users.views import send_email, send_token

router_v1 = DefaultRouter()

router_v1.register(
    'users',
    UserViewSet,
    basename='users'
)
router_v1.register(
    'genres',
    GenreViewSet,
    basename='genres'
)
router_v1.register(
    'categories',
    CategoryViewSet,
    basename='categories'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews/(?P<review_id>\d+)/comments',
    CommentsViewSet,
    basename='comments'
)
router_v1.register(
    r'titles/(?P<title_id>\d+)/reviews',
    ReviewViewSet,
    basename='reviews'
)
router_v1.register(
    'titles',
    TitleViewSet,
    basename='titles'
)

authpatterns = [
    path('email/', send_email, name='send_email'),
    path('token/', send_token, name='send_token')
]

urlpatterns = [
    path('v1/auth/', include(authpatterns)),
    path('v1/', include(router_v1.urls))
]
