from django.contrib import admin
from .models import AppUser, Item

# Register your models here.

class AdminUser(admin.ModelAdmin):
    list_display = ("full_name", "contact", "email", "password")
    search_fields = ("full_name", "contact", "email", "password")
    list_filter = ("email", "contact")

class AdminItem(admin.ModelAdmin):
        list_display = ("title", "particular", "lf", "price", "quantity", "total")
        search_fields = ("title", "particular", "lf", "price", "quantity", "total")
        list_filter = ("title", "particular", "price")

admin.site.register(AppUser, AdminUser)
admin.site.register(Item, AdminItem)

admin.site.index_title = "IMS"
admin.site.site_header = "Admin Panel"
admin.site.site_title = "Admin Panel"