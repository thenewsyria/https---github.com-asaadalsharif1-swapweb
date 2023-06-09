from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, email, full_name=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Email is required')
        user = self.model(email=self.normalize_email(email), full_name=full_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        Profile.objects.create(user=user)
        return user

    def create_superuser(self, email, full_name=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        return self.create_user(email, full_name=full_name, password=password, **extra_fields)

class User(AbstractUser):
    username = models.CharField(max_length=255, default='default_username')
    email = models.EmailField(unique=True)
    full_name = models.CharField(max_length=255, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    phone_number = models.CharField(max_length=20, default='Not Provided')
    google_id = models.CharField(max_length=255, blank=True, null=True)
    facebook_id = models.CharField(max_length=255, blank=True, null=True)
    apple_id = models.CharField(max_length=255, blank=True, null=True)
    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.email

from django.conf import settings

class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    payment_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return self.user.email

class TermsAndConditions(models.Model):
    title = models.CharField(max_length=255)
    text = models.TextField()

    def __str__(self):
        return self.title

class OTP(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    otp_code = models.CharField(max_length=6)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"OTP for {self.user.email}"


class Categorys(models.Model):
    name = models.CharField(max_length=100)
    image = models.ImageField(upload_to='image/')

class Products(models.Model):
    title = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    video = models.FileField(upload_to='videos/')
    category = models.ForeignKey(Categorys, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Favorit(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE)

    def __str__(self):
        return f"{self.user.email} - {self.product.title}"
        
from django.db import models

class Support(models.Model):
    subject = models.CharField(max_length=100)
    description = models.TextField()
    image = models.ImageField(upload_to='support/')
    status = models.CharField(max_length=20, default='In Progress')

    def __str__(self):
        return self.subject


from django.db import models
from django.utils import timezone
from .models import Support, User

from django.db import models

class Message(models.Model):
    sender = models.ForeignKey(User, related_name='sent_messages', on_delete=models.CASCADE)
    receiver = models.ForeignKey(User, related_name='received_messages', on_delete=models.CASCADE)
    product = models.ForeignKey(Products, on_delete=models.CASCADE,default=None)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"From: {self.sender.email} - To: {self.receiver.email} - Product: {self.product.title}"



from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Payment(models.Model):
    CARD_TYPES = (
        ('Visa', 'Visa'),
        ('Mastercard', 'Mastercard'),
        ('PayPal', 'PayPal'),
        ('Payoneer', 'Payoneer'),
    )

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    card_type = models.CharField(max_length=20, choices=CARD_TYPES)
    card_number = models.CharField(max_length=16)
    expiration_date = models.DateField()
    cvc = models.CharField(max_length=4)

    def __str__(self):
        return f"{self.user.email}'s {self.card_type} Card"


class Purchase(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    product = models.ForeignKey('Products', on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    timestamp = models.DateTimeField(auto_now_add=True)


## after this line I am not sure
    
# class Withdrawal(models.Model):
#     user = models.ForeignKey('User', on_delete=models.CASCADE)
#     amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])
#     created_at = models.DateTimeField(auto_now_add=True)

class Contract(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=[('pending', 'Pending'), ('completed', 'Completed')])

    def __str__(self):
        return self.title
