import uuid

from django.core.mail import send_mail
from django.db.models import Avg
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, mixins, serializers, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import (
    PageNumberPagination, LimitOffsetPagination
)
from rest_framework.permissions import (
    AllowAny, IsAuthenticated, IsAuthenticatedOrReadOnly
)
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from api.filters import TitleFilter
from api.models import Category, Genre, Review, Title, User
from api.serializers import (
    CategorySerializer, CommentsSerializer, GenreSerializer,
    ReviewSerializer, SendMessageSerializer, TitleGetSerializer,
    TitlePostSerializer, TokenSerializer, UserSerializer
)
from api.permissions import (
    IsAdmin, IsAdminOrReadOnly, IsAuthorOrStaffOrReadOnly
)
from api_yamdb.settings import EMAIL_ADMIN


@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_email(request):
    serializer = SendMessageSerializer(data=request.data)
    # confirmation_code = uuid.uuid4()
    # email = request.data.get('email')
    # username = email.replace('@', '_').lower()
    # if not User.objects.filter(email=email).exists():
    #     User.objects.create(
    #         username=username,
    #         email=email,
    #         confirmation_code=confirmation_code
    #     )
    serializer.is_valid(raise_exception=True)
    email = serializer.data.get('email')
    confirmation_code = uuid.uuid4()
    username = email.replace('@', '_').lower()
    if not User.objects.filter(email=email).exists():
        User.objects.create(
            username=username,
            email=email,
            confirmation_code=confirmation_code
        )
    send_mail(
        'Ваш код подтверждения',
        str(confirmation_code),
        EMAIL_ADMIN,
        [email]
    )
    return Response(
        {'email': f'Код для получения token отправлен на Вашу почту: {email}'}
    )


@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_token(request):
    serializer = TokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        email=serializer.data['email'],
        confirmation_code=serializer.data['confirmation_code']
    )
    refresh_token = RefreshToken.for_user(user)
    return Response({
        'token': str(refresh_token.access_token)
    })


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin, ]
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(methods=['PATCH', 'GET'], detail=False,
            permission_classes=[IsAuthenticated, ])
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=user.email, role=user.role)
        return Response(serializer.data)


class CustomViewSet(
    mixins.CreateModelMixin,
    mixins.DestroyModelMixin,
    mixins.ListModelMixin,
    viewsets.GenericViewSet
):
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [filters.SearchFilter]
    search_fields = ['=name', ]
    lookup_field = 'slug'


class GenreViewSet(CustomViewSet):
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer


class CategoryViewSet(CustomViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer


class TitleViewSet(viewsets.ModelViewSet):
    queryset = Title.objects.annotate(rating=Avg(
        'reviews__score')).order_by('-id')
    pagination_class = PageNumberPagination
    permission_classes = [IsAdminOrReadOnly, ]
    filter_backends = [DjangoFilterBackend]
    filterset_class = TitleFilter

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitlePostSerializer
        return TitleGetSerializer


class ReviewViewSet(viewsets.ModelViewSet):
    serializer_class = ReviewSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthorOrStaffOrReadOnly,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        return title.reviews.all()

    def perform_create(self, serializer):
        title = get_object_or_404(Title, pk=self.kwargs.get('title_id'))
        serializer.save(author=self.request.user, title=title)


class CommentsViewSet(viewsets.ModelViewSet):
    serializer_class = CommentsSerializer
    pagination_class = PageNumberPagination
    permission_classes = [
        IsAuthorOrStaffOrReadOnly,
        IsAuthenticatedOrReadOnly
    ]

    def get_queryset(self):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        return review.comments.all()

    def perform_create(self, serializer):
        review = get_object_or_404(Review, pk=self.kwargs.get('review_id'))
        serializer.save(author=self.request.user, review=review)
