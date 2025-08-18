from rest_framework import serializers
from .models import Report


class ReportSerializer(serializers.ModelSerializer):
    class Meta:
        model = Report
        fields = '__all__'
        read_only_fields = ('status', 'file_path', 'created_at', 'updated_at', 'requested_by')

    def create(self, validated_data):
        user = self.context['request'].user
        validated_data['requested_by'] = user
        return super().create(validated_data)