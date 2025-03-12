from django.db import models

# Shop Model
class Shop(models.Model):
    s_id = models.AutoField(primary_key=True)
    s_name = models.CharField(max_length=100)
    s_contact = models.CharField(max_length=15)
    s_email = models.EmailField(unique=True)
    s_password = models.CharField(max_length=255)

    def __str__(self):
        return self.s_name

# Customer Model
class Customer(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_name = models.CharField(max_length=100)
    c_mobile = models.CharField(max_length=15)
    c_email = models.EmailField(unique=True)
    c_pass = models.CharField(max_length=255)

    def __str__(self):
        return self.c_name

# Product Model
class Product(models.Model):
    p_id = models.AutoField(primary_key=True)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    p_name = models.CharField(max_length=100)
    p_description = models.TextField()
    p_price = models.DecimalField(max_digits=10, decimal_places=2)
    p_stock = models.IntegerField()

    def __str__(self):
        return self.name

# Order Model
class Order(models.Model):
    order_id = models.AutoField(primary_key=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    shop = models.ForeignKey(Shop, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    order_date = models.DateTimeField(auto_now_add=True)
    order_status = models.CharField(max_length=20, default="Pending")


    def __str__(self):
        return f"Order {self.id} - {self.customer.c_name} - {self.product.p_name}"

# Admin Model
class AdminUser(models.Model):
    admin_id = models.AutoField(primary_key=True)
    admin_name = models.CharField(max_length=100)
    admin_email = models.EmailField(unique=True)
    admin_password = models.CharField(max_length=255)

    def __str__(self):
        return self.admin_name
    
class Cart(models.Model):
    customer = models.ForeignKey('Customer', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    def save(self, *args, **kwargs):
        self.total_price = self.quantity * self.product.p_price
        super().save(*args, **kwargs)
