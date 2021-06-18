from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.response import Response

from .models import User
from .serializers import UserSerializer


class UserViewSet(viewsets.ModelViewSet):
    """
    User view class. Allowed only GET and PATCH methods.
    Search by username field.
    """
    queryset = User.objects.all()
    serializer_class = UserSerializer
    pagination_class = LimitOffsetPagination
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username', ]

    @action(methods=['PATCH', 'GET'], detail=False,
            url_path='me', url_name='me')
    def me(self, request, *args, **kwargs):
        user = self.request.user
        serializer = self.get_serializer(user)
        if self.request.method == 'PATCH':
            serializer = self.get_serializer(
                user, data=request.data, partial=True)
            serializer.is_valid(raise_exception=True)
            serializer.save(email=user.email, role=user.role)
        return Response(serializer.data)
