from django.urls import path
from product import views

urlpatterns = [
    path("", views.ProductListCreateView.as_view()),
    path("update-delete/<str:pk>/", views.ProductRetriveUpdateDestroyView.as_view()),
]
