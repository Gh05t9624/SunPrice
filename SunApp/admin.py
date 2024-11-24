from django.contrib import admin
from .models import CustomUser
from .models import Product
from .models import Facture
from .models import Notification


# Register your models here.
class AdminCustomUser(admin.ModelAdmin):
    list_display = ('username', 'rôle', 'genre', 'email')
admin.site.register(CustomUser, AdminCustomUser)

admin.site.register(Product)

admin.site.register(Facture)

admin.site.register(Notification)