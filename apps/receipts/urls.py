from django.urls import path
from .views import ReceiptFileUploadView, ReceiptFileValidateView, ReceiptProcessView, ReceiptListView, ReceiptDetailView

urlpatterns = [
    path('upload/', ReceiptFileUploadView.as_view(), name='upload_receipt'),
    path('validate/', ReceiptFileValidateView.as_view(), name='validate_receipt'),
    path('process/', ReceiptProcessView.as_view(), name='process_receipt'),
    path('receipts/', ReceiptListView.as_view(), name='list_receipts'),
    path('receipts/<int:id>/', ReceiptDetailView.as_view(), name='get_receipt'),
]
