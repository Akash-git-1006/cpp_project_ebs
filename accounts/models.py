from django.db import models
from django.contrib.auth.models import User
from Product_Tag_generator import extract_title_tags

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
    location = models.CharField(max_length=255)
    seller = models.ForeignKey(User,on_delete=models.CASCADE)
    seller_phone = models.CharField(max_length=15)
    date_posted = models.DateTimeField(auto_now_add=True)
    image1 = models.ImageField(upload_to='item_images/', blank=False, null=True)
    image2 = models.ImageField(upload_to='item_images/', blank=True, null=True)
    tags = models.JSONField(default=list, blank=True)  # Add this field for storing tags

    def save(self, *args, **kwargs):
    # Only generate tags for new items or if title changes
        if not self.pk:  # New item
            if self.product_title:
                self.tags = extract_title_tags(self.product_title, max_words=10)
        else:  # Existing item
            old = type(self).objects.get(pk=self.pk)
            if old.product_title != self.product_title:  
                if self.product_title:
                    self.tags = extract_title_tags(self.product_title, max_words=10)
        
        super().save(*args, **kwargs)


    def __str__(self):
        return f"Product {self.product_id}: {self.product_description}"



