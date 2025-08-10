from rest_framework import serializers
from .models import Appointment, Service


class ServiceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Service
        fields = '__all__'
        read_only_fields = ('created_at',)

    def validate_business(self, value):
        """Permission to create a service only for owner businesses"""
        request = self.context['request']
        if value.owner != request.user:
            raise serializers.ValidationError("You can only add services to your own businesses.")
        return value


class AppointmentSerializer(serializers.ModelSerializer):
    service_name = serializers.ReadOnlyField(source='service.name')
    business_name = serializers.ReadOnlyField(source='service.business.name')

    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ('created_at', 'status')

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)