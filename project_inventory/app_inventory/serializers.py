from rest_framework import serializers
from .models import AppUser, Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = ("title", "particular", "lf", "price", "quantity", "total")

class AppUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = AppUser
        fields = ("full_name", "email", "contact", "passwords")
