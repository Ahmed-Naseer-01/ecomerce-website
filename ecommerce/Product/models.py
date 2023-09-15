from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Size(models.Model):
    name = models.CharField(max_length=40)

    def __str__(self):
        return self.name

class Color(models.Model):
    name = models.CharField(max_length=30)

    def __str__(self):
        return self.name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    brand = models.CharField(max_length=100)
    description = models.TextField()
    images = models.ImageField(upload_to='product/images')
    category = models.ManyToManyField(Category, related_name='products')
    size = models.ManyToManyField(Size, related_name='products')
    color = models.ManyToManyField(Color, related_name='products')
    
    def __str__(self):
        return self.name

class Price(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    color = models.ForeignKey(Color, on_delete=models.CASCADE)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"Price for {self.product.name} ({self.color.name}): ${self.price}"
