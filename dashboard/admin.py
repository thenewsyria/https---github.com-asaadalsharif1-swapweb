from django.contrib import admin

# Register your models here.
from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import User, Category, Product, CategoryProduct, Purchase, PaymentCard, Message, SupportTicket, Withdrawal, Contract

class ProductAdmin(admin.ModelAdmin):
    list_display = ('title', 'user', 'price')

class PurchaseAdmin(admin.ModelAdmin):
    list_display = ('user', 'product', 'quantity', 'timestamp')

class PaymentCardAdmin(admin.ModelAdmin):
    list_display = ('user', 'card_number', 'exp_month', 'exp_year')

class SupportTicketAdmin(admin.ModelAdmin):
    list_display = ('user', 'subject', 'created_at')

class WithdrawalAdmin(admin.ModelAdmin):
    list_display = ('user', 'amount', 'status', 'created_at')

class ContractAdmin(admin.ModelAdmin):
    list_display = ('user', 'title', 'price', 'status')

admin.site.register(User)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(CategoryProduct)
admin.site.register(Purchase, PurchaseAdmin)
admin.site.register(PaymentCard, PaymentCardAdmin)
admin.site.register(Message)
admin.site.register(SupportTicket, SupportTicketAdmin)
admin.site.register(Withdrawal, WithdrawalAdmin)
admin.site.register(Contract, ContractAdmin)



#http://127.0.0.1:8000/admin
