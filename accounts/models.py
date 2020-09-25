from django.db import models

# Create your models here.

class Customer(models.Model):
    name = models.CharField(max_length=30, null=True)
    phone = models.CharField(max_length=30, null=True)
    email = models.CharField(max_length=30, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Indoor', 'Indoor'),
        ('Outdoor', 'Outdoor')
    )
    name = models.CharField(max_length=30, null=True)
    price = models.FloatField(null=True)
    category = models.chaname = models.CharField(max_length=30, null=True, choices=CATEGORY)
    description = models.chaname = models.CharField(max_length=30, null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for Delivery', 'Out for Delivery'),
        ('Delivered', 'Delivered')
    )
    # cutomer = 
    # product = 
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=30, choices=STATUS, null=True)