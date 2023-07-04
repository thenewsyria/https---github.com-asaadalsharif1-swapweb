from django.contrib import admin
from myapp.models import User, Categorys, Products,Support, Purchase, Payment, Message, Contract

admin.site.register(User)
admin.site.register(Categorys)
admin.site.register(Products)
admin.site.register(Purchase)
admin.site.register(Payment)
admin.site.register(Message)
admin.site.register(Contract)
admin.site.register(Support)


