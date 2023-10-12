from django.urls import path
from customer import views

urlpatterns = [
    path('',views.CustomerListCreateView.as_view()),
    path('update/<int:pk>/',views.CustomerRetriveUpdateView.as_view())
]