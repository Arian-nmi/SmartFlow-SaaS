from rest_framework import serializers
from .models import Business


class BusinessSerializer(serializers.ModelSerializer):
    class Meta:
        model = Business
        fields = ['id', 'name', 'description', 'address', 'phone', 'owner', 'created_at']
        read_only_fields = ['owner', 'created_at']