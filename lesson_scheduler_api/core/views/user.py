from core.serializers import UserSerializer
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class UserCreateView(ViewSet):
    @extend_schema(request=UserSerializer, responses={status.HTTP_201_CREATED: UserSerializer})
    def create(self, request):
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = UserSerializer(user).data
            response["id"] = user.id
            return Response(response, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
