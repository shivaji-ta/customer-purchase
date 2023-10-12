from django.db import models


class Product(models.Model):
    product_id = models.CharField(max_length=50, unique=True, primary_key=True)
    name = models.CharField(max_length=120)
    description = models.TextField()
    price = models.BigIntegerField()

    def save(self, *args, **kwargs):
        if not self.product_id:
            # Generate a unique product ID when the object is first saved
            latest_product = Product.objects.order_by("product_id").last()
            if latest_product:
                last_id = int(latest_product.product_id[1:]) + 1
            else:
                last_id = 1
            self.product_id = f"P{str(last_id).zfill(4)}"
        super(Product, self).save(*args, **kwargs)

    def __str__(self):
        return self.product_id
