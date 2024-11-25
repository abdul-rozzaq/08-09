from drf_yasg.utils import swagger_auto_schema
from rest_framework import status
from rest_framework.generics import GenericAPIView, mixins
from rest_framework.permissions import AllowAny, IsAdminUser
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken

from .models import Comment, Food, FoodType
from .permissions import IsCreator
from .serializers import (CommentSerializer, FoodSerializer,
                          FoodTypeSerializer, RegisterSerializer)


class ModelGenericAPIView(GenericAPIView):
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)


class DetailGenericAPIView(GenericAPIView):

    def get(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_object())
        return Response(serializer.data)

    def patch(self, request, *args, **kwargs):
        obj = self.get_object()

        serializer = self.get_serializer(instance=obj, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data)

    def delete(self, request, *args, **kwargs):
        obj = self.get_object()
        obj.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


class FoodAPIView(ModelGenericAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAdminUser]


class FoodDetailAPIView(DetailGenericAPIView):
    serializer_class = FoodSerializer
    queryset = Food.objects.all()
    permission_classes = [IsAdminUser]


class FoodTypeAPIView(ModelGenericAPIView):
    serializer_class = FoodTypeSerializer
    queryset = FoodType.objects.all()


class FoodTypeDetailAPIView(DetailGenericAPIView):
    serializer_class = FoodTypeSerializer
    queryset = FoodType.objects.all()


class CommentAPIView(GenericAPIView, mixins.ListModelMixin, mixins.CreateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCreator]

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


class CommentDetailAPIView(GenericAPIView, mixins.RetrieveModelMixin, mixins.DestroyModelMixin, mixins.UpdateModelMixin):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [IsCreator]

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def patch(self, request, *args, **kwargs):
        return self.partial_update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


class RegisterAPIView(GenericAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    @swagger_auto_schema(
        operation_summary="Ro'yhatdan o'tish",
        operation_id="register",
        operation_description="Ro'yxatdan o'tish uchun API",
        request_body=RegisterSerializer,
        tags=["auth"],
    )
    def post(self, request: Request, *args, **kwargs):

        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)

        return Response({"message": "User created successfully", "access_token": access_token, "refresh_token": str(refresh)})
