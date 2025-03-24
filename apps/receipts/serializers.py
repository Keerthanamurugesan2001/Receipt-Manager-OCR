from rest_framework import serializers
from .models import ReceiptFile, Receipt


class ReceiptFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = ReceiptFile
        fields = ['id', 'file_name', 'file_path', 'is_valid', 'invalid_reason', 'is_processed', 'created_at', 'updated_at']


class ReceiptSerializer(serializers.ModelSerializer):
    class Meta:
        model = Receipt
        fields = ['id', 'purchased_at', 'merchant_name', 'total_amount', 'file_path', 'created_at', 'updated_at']


class FileUploadSerializer(serializers.Serializer):
    """
    Serializer for handling file upload requests. Only the file field is required.
    """
    
    file = serializers.FileField(write_only=True)


class GetFileSerializer(serializers.Serializer):
    """
    Serializer for retrieving file data based on the file ID.
    """
    
    file_id = serializers.CharField(write_only=True)