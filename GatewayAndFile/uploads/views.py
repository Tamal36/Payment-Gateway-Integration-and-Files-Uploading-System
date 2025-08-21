import requests
from django.urls import reverse
from django.shortcuts import render, redirect
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from django.views.decorators.csrf import csrf_protect
from django.contrib.auth.decorators import login_required
from rest_framework import status
from .models import *
from payments.models import *
from .serializers import *
from .tasks import *
import os

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def upload_file(request):
    user_profile = request.user.profile
    
    # Check at least one successful transaction
    if not user_profile.transactions.filter(status=2).exists():
        return Response({"error": "Payment required before uploading"}, status=403)

    # Validate file extension
    uploaded_file = request.FILES.get('file')
    if not uploaded_file:
        return Response({"error": "No file uploaded."}, status=400)

    allowed_extensions = ['.txt', '.docx']
    ext = os.path.splitext(uploaded_file.name)[1].lower()
    if ext not in allowed_extensions:
        return Response({"error": "Invalid file type. Only .txt and .docx are allowed."}, status=400)

    # Proceed 
    serializer = FileUploadSerializer(data=request.data)
    if serializer.is_valid():
        file_obj = serializer.save(
            user_profile=user_profile,
            filename=uploaded_file.name
        )
        process_file.delay(file_obj.id)
        return Response(FileUploadSerializer(file_obj).data, status=status.HTTP_201_CREATED)

    return Response(serializer.errors, status=400)

@csrf_protect
@login_required
def upload_view(request):
    if request.method == 'POST':
        file = request.FILES.get('file')
        
        if not file:
            return render(request, 'uploads/upload.html', {'error': 'No file selected'})
        
        upload_url = request.build_absolute_uri(reverse('upload-file'))
        
        response = requests.post(
            upload_url,
            files={'file': file},
            cookies=request.COOKIES  # use headers if auth is needed
        )
        
        print("Upload status code:", response.status_code)
        print("Upload response text:", response.text)
        
        if response.status_code == 201:
            return render(request, 'uploads/upload.html', {'success': 'File uploaded successfully!'})
        
        return render(request, 'uploads/upload.html', {
            'error': 'Upload failed.',
            'details': response.json() if response.headers.get('content-type') == 'application/json' else response.text
        })
        
    return render(request, 'uploads/upload.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_files(request):
    files = request.user.profile.uploads.all()
    serializer = FileUploadSerializer(files, many=True)
    return Response(serializer.data)

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def list_activity(request):
    logs = request.user.profile.activity_logs.all()
    serializer = ActivityLogSerializer(logs, many=True)
    return Response(serializer.data)

@login_required
def upload_file_view(request):
    has_paid = PaymentTransaction.objects.filter(
        user_profile__user=request.user,
        status=PaymentTransaction.STATUS_SUCCESS
    ).exists()
    
    context = {
        'has_paid': has_paid
    }
    return render(request, 'uploads/upload.html', context)


@login_required
def list_files_view(request):
    files = request.user.profile.uploads.all().order_by('-upload_time')
    context = {
        'files': files
    }
    return render(request, 'uploads/files.html', context)

@login_required
def list_activity_view(request):
    logs = request.user.profile.activity_logs.all().order_by('-timestamp')
    context = {
        'logs': logs
    }
    return render(request, 'uploads/activity.html', context)