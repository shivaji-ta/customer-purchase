from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from customer.serializers import  User
from product.models import Product
from coupon.models import Coupon
from .models import Cart, OrderModel, OrderDetailsModel
from .serializers import CartSerializer, OrderSerializer, OrderDetailsSerializer


class CartView(APIView):
    def get_product(self, id):
        try:
            return Product.objects.get(pk=id)
        except:
            return None

    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None

    def get(self, request, user_id):
        customer = self.get_user(user_id)
        if not customer:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        items = Cart.objects.filter(customer=customer)
        serializer = CartSerializer(items, many=True, context={"request": request})
        cart_total = items.aggregate(Sum("amount"))["amount__sum"]
        return Response(
            {"items": serializer.data, "cart_total": cart_total},
            status=status.HTTP_200_OK,
        )

    def post(self, request, user_id):
        product = self.get_product(request.POST.get("product_id"))
        customer = self.get_user(user_id)
        quantity = request.POST.get("quantity")
        if not product:
            return Response(
                {"error": "Product not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not customer:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        if not quantity:
            return Response(
                {"error": "Quantity is required"}, status=status.HTTP_404_NOT_FOUND
            )
        cart, created = Cart.objects.get_or_create(product=product, customer=customer)
        cart.quantity = int(quantity)
        cart.save()
        items = Cart.objects.filter(customer=customer)
        serializer = CartSerializer(items, many=True, context={"request": request})
        cart_total = items.aggregate(Sum("amount"))["amount__sum"]
        return Response(
            {"items": serializer.data, "cart_total": cart_total},
            status=status.HTTP_201_CREATED,
        )


class ApplyCouponView(APIView):
    def get_user(self, id):
        try:
            return User.objects.get(pk=id)
        except:
            return None

    def get_coupon(self, code):
        try:
            return Coupon.objects.get(code=code)
        except:
            return None

    def get(self, request, user_id):
        customer = self.get_user(user_id)
        if not customer:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        items = Cart.objects.filter(customer=customer)
        if items.count() < 1:
            return Response(
                {"error": "No items in Cart"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CartSerializer(items, many=True, context={"request": request})
        discount = 0
        pb_discount = items.aggregate(Sum("amount"))["amount__sum"]
        pa_discount = pb_discount - discount
        return Response(
            {
                "items": serializer.data,
                "pb_discount": pb_discount,
                "discount": discount,
                "pa_discount": pa_discount,
            },
            status=status.HTTP_201_CREATED,
        )

    def post(self, request, user_id):
        customer = self.get_user(user_id)
        if not customer:
            return Response(
                {"error": "Customer not found"}, status=status.HTTP_404_NOT_FOUND
            )
        coupon = self.get_coupon(request.POST.get("coupon"))
        items = Cart.objects.filter(customer=customer)
        if items.count() < 1:
            return Response(
                {"error": "No items in Cart"}, status=status.HTTP_404_NOT_FOUND
            )
        serializer = CartSerializer(items, many=True, context={"request": request})
        discount = coupon.discount
        pb_discount = items.aggregate(Sum("amount"))["amount__sum"]
        pa_discount = pb_discount - discount
        return Response(
            {
                "items": serializer.data,
                "pb_discount": pb_discount,
                "discount": discount,
                "pa_discount": pa_discount,
            },
            status=status.HTTP_201_CREATED,
        )


class PlaceOrderView(APIView):
    def get_customer(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except:
            return None

    def get_coupon(self, code):
        try:
            return Coupon.objects.get(code=code)
        except:
            return None

    def post(self, request, user_id):
        customer = self.get_customer(user_id)
        coupon = self.get_coupon(request.POST.get("coupon"))
        if coupon:
            discount = coupon.discount
            code = coupon.code
        else:
            discount = 0
            code = "No Coupon Applied"
        items = Cart.objects.filter(customer=customer)
        if items.count() < 1:
            return Response(
                {"error": "No items in Cart"}, status=status.HTTP_404_NOT_FOUND
            )
        pb_discount = items.aggregate(Sum("amount"))["amount__sum"]
        pa_discount = pb_discount - discount
        order = OrderModel.objects.create(
            customer=customer,
            pb_discount=pb_discount,
            pa_discount=pa_discount,
            discount=discount,
            discount_code=code,
        )
        order_details = []
        for item in items:
            order_details.append(
                OrderDetailsModel(
                    product_name=item.product.name,
                    product_desc=item.product.description,
                    product_price=item.product.price,
                    product_quantity=item.quantity,
                    product_amount=item.product.price * item.quantity,
                    order_id=order.order_id,
                )
            )
            item.delete()
        OrderDetailsModel.objects.bulk_create(order_details)
        products = order_details
        ord_serializer = OrderSerializer(order)
        prod_serializer = OrderDetailsSerializer(products, many=True)
        return Response(
            {"order_details": ord_serializer.data, "products": prod_serializer.data}
        )
