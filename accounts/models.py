from django.db import models
from django.contrib.auth.models import User


class item (models.Model):

    CATEGORY_CHOICES = [
        ('Electronics', 'Electronics'),
        ('Furniture', 'Furniture'),
        ('Clothing', 'Clothing'),
        ('Books', 'Books'),
        ('Other', 'Other'),
    ]

    CONDITION_CHOICES = [
        ('New', 'New'),
        ('Used', 'Used'),
        ('Refurbished', 'Refurbished'),
    ]
    product_title = models.CharField(max_length=255)
    product_id = models.AutoField(primary_key=True)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    product_description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    # product_condition = models.CharField(max_length=50, choices=CONDITION_CHOICES)
    location = models.CharField(max_length=255)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    seller_phone = models.CharField(max_length=15)
    date_posted = models.DateTimeField(auto_now_add=True)
    image1 = models.ImageField(upload_to='item_images/', blank=False, null=True)
    image2 = models.ImageField(upload_to='item_images/', blank=True, null=True)


    def __str__(self):
        return f"Product {self.product_id}: {self.product_description}"



