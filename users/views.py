import uuid

from api_yamdb.settings import EMAIL_ADMIN
from django.core import exceptions
from django.core.mail import send_mail
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from users.models import User
from users.serializers import SendMessageSerializer, TokenSerializer


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
