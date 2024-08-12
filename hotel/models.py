from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Customer(models.Model):
    customer = models.ForeignKey(User, on_delete=models.CASCADE)
    orders = models.IntegerField(default=0)
    total_sale = models.IntegerField(default=0)

    def __str__(self):
        return self.customer.email

class Staff(models.Model):
    admin = 'Admin'

    ROLES = (
        (admin,admin),
    )
    
    staff_id = models.ForeignKey(User, on_delete=models.CASCADE)
    email = User.email
    role = models.CharField(max_length = 30, choices = ROLES)
    
    def __str__(self):
        return self.staff_id.email

class Order(models.Model):
    pending = 'Pending'
    completed = 'Completed'

    STATUS = (
        (pending,pending),
        (completed,completed),
    )

    customer = models.ForeignKey(Customer,on_delete=models.CASCADE)
    order_timestamp = models.DateTimeField(auto_now_add=True)
    delivery_status = models.CharField(max_length = 100, choices = STATUS)
    if_cancelled = models.BooleanField(default = False)
    total_amount = models.IntegerField()

    def confirmDelivery(self):
        self.delivery_status = self.completed
        self.save()
    
    def __str__(self):
        return self.customer.__str__()

class Food(models.Model):

    disabled = 'Disabled'
    enabled = 'Enabled'

    STATUS = (
        (disabled, disabled),
        (enabled, enabled),
    )

    name = models.CharField(max_length=250)
    status = models.CharField(max_length=50, choices=STATUS)
    content_description = models.TextField()
    sale_price = models.FloatField()
    image = models.FileField(blank=True, null =True)
    num_order = models.IntegerField(default=0)
    quantity_available = models.IntegerField()

    def __str__(self):
        return self.name

class OrderContent(models.Model):
    quantity = models.IntegerField(default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    order = models.ForeignKey(Order, on_delete=models.CASCADE)

class Cart(models.Model):
    quantity = models.IntegerField(default=1)
    food = models.ForeignKey(Food, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
