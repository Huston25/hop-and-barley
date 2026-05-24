from django.db import models

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    parent = models.ForeignKey('self',
                               on_delete=models.CASCADE,
                               null=True, blank=True,
                               related_name='children')
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(max_length=100, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE,
                                related_name='products')
    description = models.TextField()
    short_description = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='product_images/')
    is_active = models.BooleanField(default=True)
    stock = models.IntegerField()
    specifications = models.JSONField(blank=True, null=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now=True)

    def __str__(self):
        return self.name



class Review(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='reviews')
    name = models.CharField(max_length=100)
    rating = models.PositiveSmallIntegerField()
    title = models.CharField(max_length=100)
    text = models.TextField()
    avatar = models.ImageField(upload_to='product_avatars/', null=True, blank=True)
    created_at = models.DateField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'{self.product.name} - {self.rating} - {self.name}'
