from rest_framework import serializers
from .models import Appointment, Service
from django.utils import timezone


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

    def validate(self, attrs):
        service = attrs['service']
        date = attrs['date']
        time = attrs['time']
        user = self.context['request'].user

        existing_count = Appointment.objects.filter(
            service=service,
            date=date,
            time=time
        ).count()
        if existing_count >= service.capacity:
            raise serializers.ValidationError("This hour is full.")

        if Appointment.objects.filter(
            user=user,
            date=date,
            time=time
        ).exists():
            raise serializers.ValidationError("You have already booked an appointment at this time.")

        return attrs

    def create(self, validated_data):
        validated_data['user'] = self.context['request'].user
        return super().create(validated_data)