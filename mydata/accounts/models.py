from django.db import models
from django.contrib.auth.models import User
# Create your models here.


class Customer(models.Model):
    user = models.OneToOneField(User, blank=True, null=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, null=True)
    phone = models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200, null=True)
    profile_pic = models.ImageField(default="IMG_20191128_200516_319.jpg", null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Product(models.Model):
    CATEGORY = (
        ('Coffee And Shakes', 'Coffee And Shakes'),
        ('Roll', 'Roll'),
        ('Starters', 'Fried Rice'),
        ('Fast Food', 'Fast Food'),
        ('Momos', 'Momos'),
        ('Noodles', 'Noodles'),
        ('Manchurian', 'Manchurian'),
        ('Sandwich', 'Sandwich'),
        ('Soup', 'Soup'),
        ('Starters', 'Starters'),
        ('Non-Veg Main Course', 'Non-Veg Main Course'),
        ('Biryani', 'Biryani'),
        ('Indian Sabji', 'Indian Sabji'),
        ('Roti / Paratha', 'Roti / Paratha'),
        ('EGG', 'EGG'),
        ('DAL', 'DAL'),
        ('Rice', 'Rice'),
        ('South Indian', 'South Indian'),
        ('THALI', 'THALI'),
    )

    name = models.CharField(max_length=200, null=True)
    price = models.FloatField(null=True)
    category = models.CharField(max_length=200, null=True, choices=CATEGORY)
    description = models.CharField(max_length=200, null=True, blank=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name


class Order(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out for delivery', 'Out for delivery'),
        ('Delivered', 'Delivered'),
    )

    customer = models.ForeignKey(Customer, null=True, on_delete=models.SET_NULL)
    product = models.ForeignKey(Product, null=True, on_delete=models.SET_NULL)
    date_created = models.DateTimeField(auto_now_add=True, null=True)
    status = models.CharField(max_length=200, null=True, choices=STATUS)
    note = models.CharField(max_length=1000, null=True)

    def __str__(self):
        return self.customer.name


