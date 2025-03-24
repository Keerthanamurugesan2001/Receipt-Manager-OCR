from django.core.files.storage import FileSystemStorage
from drf_yasg.utils import swagger_auto_schema

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser

from .models import ReceiptFile, Receipt
from .serializers import (ReceiptFileSerializer, ReceiptSerializer, FileUploadSerializer, GetFileSerializer)
from .utils.common import is_valid_pdf, extract_text_from_pdf


class ReceiptFileUploadView(APIView):
    """ 
    Upload Receipt file
    """
    parser_classes = [MultiPartParser, FormParser]

    @swagger_auto_schema(
        operation_description="Upload a receipt file",
        request_body=FileUploadSerializer, 
    )
    def post(self, request):
        """
        Upload the file in the input directory.
        """
        serializer = FileUploadSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.validated_data['file']
            fs = FileSystemStorage()
            file_name = 'input/'+file.name
            file_path = fs.save(file_name, file)

            receipt_file = ReceiptFile.objects.create(
                file_name=file_name,
                file_path=file_path,
                is_valid=False,
                is_processed=False
            )

            serializer = ReceiptFileSerializer(receipt_file)
        return Response({"message": "File uploaded successfully", "file_id": receipt_file.id}, status=status.HTTP_201_CREATED)


class ReceiptFileValidateView(APIView):

    @swagger_auto_schema(
        operation_description="Validate a receipt file",
        request_body=GetFileSerializer,
    )
    def post(self, request):
        """
        Validate the file based on ID
        """
        serializer = GetFileSerializer(data=request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['file_id']
            try:
                receipt_file = ReceiptFile.objects.get(id=file_id)
            except ReceiptFile.DoesNotExist:
                return Response({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)

            file_path = receipt_file.file_path
            is_valid = is_valid_pdf(file_path)

            receipt_file.is_valid = is_valid
            response = {"is_valid": is_valid}
            if not is_valid:
                receipt_file.invalid_reason = "Invalid PDF"
                response['invalid_reason']=receipt_file.invalid_reason
            receipt_file.save()
            
            return Response(response,
            status=status.HTTP_200_OK)


class ReceiptProcessView(APIView):

    @swagger_auto_schema(
        operation_description="Process a receipt file",
        request_body=GetFileSerializer,
    )
    def post(self, request):
        """
        Extract the valid data from the uploaded file
        """
        serializer = GetFileSerializer(data=request.data)
        if serializer.is_valid():
            file_id = serializer.validated_data['file_id']

            try:
                receipt_file = ReceiptFile.objects.get(id=file_id)
            except ReceiptFile.DoesNotExist:
                return Response({"message": "File not found"}, status=status.HTTP_404_NOT_FOUND)

            if not receipt_file.is_valid:
                return Response({"message": "Invalid receipt file"}, status=status.HTTP_400_BAD_REQUEST)


            extracted_data = extract_text_from_pdf(receipt_file.file_path)

            receipt = Receipt.objects.create(
                purchased_at=extracted_data.get('processed_date'),
                merchant_name=extracted_data.get('merchant_name'),
                total_amount=extracted_data.get('total_amount'),
                file_path=receipt_file.file_path
            )
            receipt_file.is_processed = True
            receipt_file.save()

            return Response({
                "message": "Receipt processed successfully",
                "receipt_id": ReceiptSerializer(receipt)
            }, status=status.HTTP_201_CREATED)


class ReceiptListView(APIView):
    def get(self, request):
        """
        List all the Receipt
        """
        receipts = Receipt.objects.all()
        serializer = ReceiptSerializer(receipts, many=True)
        return Response({"receipts": serializer.data})


class ReceiptDetailView(APIView):
    def get(self, request, id):
        """
        Show the full detail of Receipt
        """
        try:
            receipt = Receipt.objects.get(id=id)
            serializer = ReceiptSerializer(receipt)
            return Response({"receipt": serializer.data})
        except Receipt.DoesNotExist:
            return Response({"message": "Receipt not found"}, status=status.HTTP_404_NOT_FOUND)
