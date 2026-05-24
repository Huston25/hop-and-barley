from django.db import models

# Create your models here.
class Order(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    status = models.CharField(
        choices=(
            ('pending', 'Pending'),
             ('paid', 'Paid'),
             ('shipped', 'Shipped'),
             ('delivered', 'Delivered'),
             ('cancelled', 'Cancelled'))
    )
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey('products.Product', on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)