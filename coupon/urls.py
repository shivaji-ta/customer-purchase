from django.urls import path
from . import views

urlpatterns = [
    path("", views.CouponListCreateView.as_view()),
    path("update-delete/<int:pk>/", views.CouponRetriveUpdateDestroyView.as_view()),
]
