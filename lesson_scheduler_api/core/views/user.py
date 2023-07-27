from core.serializers import LoginSerializer, RegisterSerializer, UserSerializer
from drf_spectacular.utils import extend_schema
from knox.models import AuthToken
from rest_framework import generics
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
    def signup_action(self, request, *args, **kwargs):
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
    def signin_action(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data
        return Response(
            {
                "user": UserSerializer(user, context=self.get_serializer_context()).data,
                "token": AuthToken.objects.create(user)[1],
            }
        )
