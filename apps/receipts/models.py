from django.db import models


class ReceiptFile(models.Model):
    """
    Represents a receipt file uploaded by the user.
    """
    
    id = models.AutoField(primary_key=True)
    file_name = models.CharField(max_length=255)
    file_path = models.CharField(max_length=255)
    is_valid = models.BooleanField(default=False)
    invalid_reason = models.TextField(null=True, blank=True)
    is_processed = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.file_name


class Receipt(models.Model):
    """
    Represents a receipt with purchase details.
    """
    id = models.AutoField(primary_key=True)
    purchased_at = models.DateTimeField()
    merchant_name = models.CharField(max_length=255)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    file_path = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Receipt from {self.merchant_name} on {self.purchased_at}"
