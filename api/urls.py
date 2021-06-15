from django.urls import include, path
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import (TokenObtainPairView,
                                            TokenRefreshView)

from .views import GenreViewSet, CategoryViewSet, TitleViewSet


router = DefaultRouter()
router.register('/genres', GenreViewSet, basename='genres')
router.register('/categories', CategoryViewSet, basename='categories')
router.register('/titles', TitleViewSet, basename='titles')

urlpatterns = [
    path('auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include(router.urls)),
]
