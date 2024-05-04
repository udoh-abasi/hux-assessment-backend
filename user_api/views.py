from django.contrib.auth import login, logout, get_user_model
from rest_framework.authentication import SessionAuthentication
from rest_framework.views import APIView
from rest_framework.response import Response
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_protect
from .serializers import (
    UserSerializer,
    UserLoginSerializer,
    UserRegisterSerializer,
)
from .validation import (
    custom_validation,
    validate_email,
    validate_password,
)
from rest_framework import permissions, status
from .permissions import UserAlreadyExistPermission
from django.core.exceptions import ValidationError


User = get_user_model()


# @method_decorator(csrf_protect, name="dispatch")
class UserRegister(APIView):
    permission_classes = (
        UserAlreadyExistPermission,
        permissions.AllowAny,
    )

    def post(self, request):
        try:
            clean_data = custom_validation(request.data)

        except:
            return Response(
                {"message": "Email already exist or password is invalid"},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = UserRegisterSerializer(data=clean_data)

        if serializer.is_valid(raise_exception=True):
            user = serializer.create(clean_data)
            if user:
                return Response(
                    serializer.data["email"], status=status.HTTP_201_CREATED
                )
            return Response(status=status.HTTP_400_BAD_REQUEST)


# @method_decorator(csrf_protect, name="dispatch")
class UserLogin(APIView):
    permission_classes = (permissions.AllowAny,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        data = request.data

        try:
            assert validate_email(data)
            assert validate_password(data)
        except:
            return Response(
                {
                    "message": "Invalid email or password",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        try:
            serializer = UserLoginSerializer(data=data)
            if serializer.is_valid(raise_exception=True):
                user = serializer.check_user(data)
                login(request, user)
                return Response(serializer.data["email"], status=status.HTTP_200_OK)
        except ValidationError:
            return Response(
                {
                    "message": "User not found",
                },
                status=status.HTTP_404_NOT_FOUND,
            )

        except:
            return Response(
                {
                    "message": "Something went wrong",
                },
                status=status.HTTP_400_BAD_REQUEST,
            )


@method_decorator(csrf_protect, name="dispatch")
class UserLogout(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def post(self, request):
        logout(request)
        return Response(status=status.HTTP_200_OK)


@method_decorator(csrf_protect, name="dispatch")
class UserView(APIView):
    permission_classes = (permissions.IsAuthenticated,)
    authentication_classes = (SessionAuthentication,)

    def get(self, request):
        serializer = UserSerializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)
