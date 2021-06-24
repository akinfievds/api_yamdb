import uuid

from api_yamdb.settings import EMAIL_ADMIN
from django.core import exceptions
from django.core.mail import send_mail
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.permissions import IsAdmin
from users.serializers import (
    SendMessageSerializer, TokenSerializer, UserSerializer
)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_email(request):
    serializer = SendMessageSerializer(data=request.data)
    if serializer.is_valid():
        email = serializer.data.get('email')
        email_divided = email.split('@')
        username = str(email_divided[0] + f'_{email_divided[1]}').capitalize()
        confirmation_code = uuid.uuid4()
        User.objects.create(
            username=username,
            email=email
        )
        send_mail(
            'Ваш код подтверждения',
            str(confirmation_code),
            EMAIL_ADMIN,
            [email]
        )
        return Response(
            {'email': f'Пароль отправлен на вашу почту: {email}'}
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes((AllowAny, ))
def send_token(request):
    serializer = TokenSerializer(data=request.data)
    if serializer.is_valid():
        try:
            user = User.objects.get(
                email=serializer.data['email'],
                confirmation_code=serializer.data['confirmation_code']
            )
            refresh_token = RefreshToken.for_user(user)
            return Response({
                'token': str(refresh_token.access_token)
            })
        except exceptions.ObjectDoesNotExist:
            return Response(
                data={
                    'detail': 'Пользователь с переданнымы данными не найден'
                },
                status=status.HTTP_400_BAD_REQUEST
            )


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
