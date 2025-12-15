from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters

from apps.manager_admin.serializers.user import UserSerializer
from apps.user.models import User
from core.pagination_handler import DefaultPagination
from core.permission import IsAdmin


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdmin]
    pagination_class = DefaultPagination
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['username']
    filterset_fields = ['username']
