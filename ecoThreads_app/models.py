from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class City(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Area(models.Model):
    name = models.CharField(max_length=200)
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=True)

    def __str__(self):
        return self.name

class Address(models.Model):
    area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, blank=True)
    pin_code = models.PositiveIntegerField()
    latitude = models.FloatField()
    longitude = models.FloatField()

    def __str__(self):
        return f"{self.area.name}, {self.area.city.name}"

class Orders(models.Model):
    STATUS = (
        ('Pending', 'Pending'),
        ('Out to collect', 'Out to collect'),
        ('Collected', 'Collected'),
    )

    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
    order_name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='photos/')
    status = models.CharField(max_length=200, default='Pending', choices=STATUS)

    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)

    address = models.ForeignKey(Address, on_delete=models.SET_NULL, null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)

    class Meta:
        ordering = ['-created_at','-modified_at']

    def save(self, *args, **kwargs):
        # Set created_at and modified_at to IST
        if not self.pk:  # Set only during creation
            self.created_at = timezone.localtime(timezone.now())
        self.modified_at = timezone.localtime(timezone.now())

        super(Orders, self).save(*args, **kwargs)

    def __str__(self):
        return self.order_name

# class Photo(models.Model):
#     image = models.ImageField(upload_to='photos/')
#     order = models.ForeignKey(Orders, on_delete=models.CASCADE)
