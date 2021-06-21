import uuid

from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from django.core.management.utils import get_random_secret_key
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import TokenObtainPairView

from users.models import User
from users.permissions import IsAdmin, IsAllRolesOrReadOnly
from users.serializers import (SendMessageSerializer, TokenSerializer,
                               UserSerializer)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_email(request):
    serializer = SendMessageSerializer(data=request.data)
    email = request.data.get('email')
    if serializer.is_valid(raise_exception=True):
        email = serializer.data.get('email')
        username = email.split('@')[0]
        password = str(get_random_secret_key())[:8]
        password_hash = make_password(password)
        confirmation_code = uuid.uuid4()
        User.objects.create_user(
            username=username,
            email=email,
            password=password_hash,
            confirmation_code=confirmation_code
        )
        send_mail(
            'Ваш код подтверждения',
            str(confirmation_code),
            'admin@admin.ru',
            [email]
        )
        return Response(
            {'email': f'Пароль отправлен на вашу почту: {email}'}
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


class TokenObtainView(TokenObtainPairView):
    permission_classes = [AllowAny, ]

    def post(self, *args, **kwargs):
        serializer = TokenSerializer(data=self.request.data)
        serializer.is_valid(raise_exception=True)
        user = User.objects.get(
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
            permission_classes=[IsAuthenticated, IsAllRolesOrReadOnly, ])
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=user.email, role=user.role)
        return Response(serializer.data)
