from django.db import models
from customer.models import User
from product.models import Product
from django.db.models.signals import pre_save
from django.dispatch import receiver


class Cart(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=1)
    amount = models.BigIntegerField()


@receiver(pre_save, sender=Cart)
def cart_amount_handler(sender, instance, *args, **kwargs):
    instance.amount = instance.product.price * instance.quantity


class OrderModel(models.Model):
    order_id = models.CharField(max_length=15, primary_key=True, unique=True)
    customer = models.ForeignKey(User, on_delete=models.PROTECT)
    pb_discount = models.BigIntegerField()
    pa_discount = models.BigIntegerField()
    discount = models.IntegerField()
    discount_code = models.CharField(max_length=50, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.order_id:
            # Generate a unique order ID when the object is first saved
            latest_order = OrderModel.objects.order_by("order_id").last()
            if latest_order:
                last_id = int(latest_order.order_id[2:]) + 1
            else:
                last_id = 1
            self.order_id = f"OD{str(last_id).zfill(5)}"
        super(OrderModel, self).save(*args, **kwargs)


class OrderDetailsModel(models.Model):
    product_name = models.CharField(max_length=50)
    product_desc = models.TextField()
    product_price = models.BigIntegerField()
    product_quantity = models.IntegerField()
    product_amount = models.BigIntegerField()
    order_id = models.CharField(max_length=50)
