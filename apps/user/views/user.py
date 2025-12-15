from rest_framework.response import Response
from rest_framework.views import APIView

from apps.user.serializers.user import UserProfileSerializer
from core.permission import IsSeller


class UserProfileView(APIView):
    permission_classes = [IsSeller]

    def get(self, request):
        user = request.user
        serializer = UserProfileSerializer(user)
        return Response(serializer.data)
