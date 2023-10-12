from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView
from .models import Coupon
from .serializers import CouponSerializer


class CouponListCreateView(ListCreateAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer


class CouponRetriveUpdateDestroyView(RetrieveUpdateDestroyAPIView):
    queryset = Coupon.objects.all()
    serializer_class = CouponSerializer
