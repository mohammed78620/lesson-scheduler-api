from core.models import User
from core.serializers import LoginSerializer, RegisterSerializer, UpdatePasswordSerializer, UserSerializer
from drf_spectacular.utils import extend_schema
from knox.models import AuthToken
from rest_framework import generics, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.viewsets import ViewSet


class SignUpAPI(ViewSet, generics.GenericAPIView):
    serializer_class = RegisterSerializer

    @action(detail=False, methods=["post"])
    @extend_schema(
        request=RegisterSerializer,
        responses={200: UserSerializer},
        description="Sign Up",
    )
    def signup(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        token = AuthToken.objects.create(user)
        return Response({"users": UserSerializer(user, context=self.get_serializer_context()).data, "token": token[1]})


class SignInAPI(ViewSet, generics.GenericAPIView):
    serializer_class = LoginSerializer

    @action(detail=False, methods=["post"])
    @extend_schema(
        request=LoginSerializer,
        responses={200: UserSerializer},
        description="Sign In",
    )
    def signin(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )


class UpdateUserDetails(ViewSet):
    @extend_schema(
        request=UpdatePasswordSerializer,
    )
    @action(detail=False, methods=["post"])
    def update_password(self, request):
        request_data = request.data
        old_password = request_data.get("old_password", None)
        new_password = request_data.get("new_password", None)

        if not any([old_password, new_password]):
            return Response({"error": "old or new password cannot be empty"}, status.HTTP_400_BAD_REQUEST)

        elif old_password == new_password:
            return Response({"error": "old and new password cannot be the same"}, status.HTTP_400_BAD_REQUEST)

        username = request_data.get("username", None)
        try:
            user = User.objects.get(username=username)
            user.password = new_password
            user.save()

        except Exception:
            return Response({"error": "User not found"}, status=status.HTTP_404_NOT_FOUND)

        return Response({"message": "password updated"}, status.HTTP_200_OK)
