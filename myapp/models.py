from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, password, **extra_fields)

class User(AbstractBaseUser):
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

class Product(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products')
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    categories = models.ManyToManyField('Category', through='CategoryProduct')

    def __str__(self):
        return self.title

class CategoryProduct(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)

class Purchase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Product', on_delete=models.CASCADE)
    payment_card = models.ForeignKey('PaymentCard', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)

class PaymentCard(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    card_number = models.CharField(max_length=16)
    exp_month = models.PositiveIntegerField()
    exp_year = models.PositiveIntegerField()

class Message(models.Model):
    sender = models.ForeignKey('User', related_name='sent_messages', on_delete=models.CASCADE)
    recipient = models.ForeignKey('User', related_name='received_messages', on_delete=models.CASCADE)
    text = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

class SupportTicket(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    subject = models.CharField(max_length=255)
    message = models.TextField()
    attachment = models.FileField(upload_to='support_tickets', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

class Withdrawal(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
    created_at = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return self.title