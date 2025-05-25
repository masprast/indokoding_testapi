from django.contrib.auth import get_user_model
from rest_framework import status, viewsets
from rest_framework.generics import CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAdminUser, IsAuthenticated
from rest_framework.response import Response

from test_api.permissions import IsAdminOrReadOnly

from .serializers import (UserCreateSerializer, UserProfileAdminSerializer,
                          UserProfilePublicSerializer, UserSerializer)

PostUser = get_user_model()


# Create your views here.
class UserViewSet(viewsets.ModelViewSet):
    queryset = PostUser.objects.all().order_by("-date_joined")
    serializer_class = UserSerializer
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.action == "create":
            return UserCreateSerializer
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data, status=status.HTTP_201_CREATED, headers=headers
        )


class UserRegisterView(CreateAPIView):
    queryset = PostUser.objects.all()
    serializer_class = UserCreateSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        return Response(
            {
                "message": "Berhasil registrasi",
                "user_id": user.id,
                "username": user.username,
                "email": user.email,
            },
            status=status.HTTP_201_CREATED,
        )


class UserProfilePublicVew(RetrieveAPIView):
    queryset = PostUser.objects.all()
    serializer_class = UserProfilePublicSerializer
    permission_classes = [AllowAny]
    lookup_field = "username"


class UserProfileAdminView(RetrieveAPIView):
    queryset = PostUser.objects.all()
    serializer_class = UserProfileAdminSerializer
    permission_classes = [IsAdminUser]
    lookup_field = "username"
