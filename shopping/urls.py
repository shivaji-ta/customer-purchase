from django.urls import path
from . import views

urlpatterns = [
    path('cart/<int:user_id>/',views.CartView.as_view()),
    path('apply-coupon/<int:user_id>/',views.ApplyCouponView.as_view()),
    path('place-order/<int:user_id>/',views.PlaceOrderView.as_view())
]