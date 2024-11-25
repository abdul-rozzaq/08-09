from django.urls import path

from .views import CommentAPIView, CommentDetailAPIView, FoodAPIView, FoodDetailAPIView, FoodTypeAPIView, FoodTypeDetailAPIView, RegisterAPIView

urlpatterns = [
    path("food-type/", FoodTypeAPIView.as_view()),
    path("food-type/<int:pk>/", FoodTypeDetailAPIView.as_view()),
    #
    path("food/", FoodAPIView.as_view()),
    path("food/<int:pk>/", FoodDetailAPIView.as_view()),
    #
    path("comment/", CommentAPIView.as_view()),
    path("comment/<int:pk>/", CommentDetailAPIView.as_view()),
    #
    path("register/", RegisterAPIView.as_view()),
]
