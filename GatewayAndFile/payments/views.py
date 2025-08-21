import requests, uuid
from django.shortcuts import render
from django.http import HttpResponse
from django.conf import settings
from django.shortcuts import redirect
from django.contrib.auth import authenticate, login
from rest_framework.decorators import api_view, permission_classes
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from .models import *
from .serializers import *
# Create your views here.

@api_view(['POST'])
@permission_classes([AllowAny])
def register_user(request):
    serializer = UserRegistrationSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=201)
    return Response(serializer.errors, status=400)

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('transaction-history-view')
        else:
            return HttpResponse("Invalid credentials. <a href='/api/login-view/'>Try again</a>")
    return render(request, 'payments/login.html')

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    profile = request.user.profile 
    serializer = UserProfileSerializer(profile)
    return Response(serializer.data)

@api_view(['POST'])
@permission_classes([IsAuthenticated])
def initiate_payment(request):
    user = request.user
    transaction_id = str(uuid.uuid4()).replace('-', '')[:32]

    amount = 100.00  # ⚠️ 

    if amount != 100.00:
        return Response(
            {"error": "Invalid amount. Amount must be exactly 100"},
            status=400
        )

    payload = {
        "store_id"      : settings.STORE_ID,
        "signature_key" : settings.SIGNATURE_KEY,
        "tran_id"       : transaction_id,
        "success_url"   : request.build_absolute_uri("/api/payment/success/"),
        "fail_url"      : request.build_absolute_uri("/api/payment/failed/"),
        "cancel_url"    : request.build_absolute_uri("/api/payment/cancelled/"),
        "amount"        : str(amount),
        "currency"      : "BDT",
        "desc"          : "File Upload Payment",
        "cus_name"      : user.username,
        "cus_email"     : user.email or "test@example.com",
        "cus_phone"     : "01700000000",
        "type"          : "json"
    }

    try:
        r = requests.post(settings.AAMARPAY_ENDPOINT, json=payload)
        data = r.json()
    except Exception as e:
        return Response({
            "error": "Failed to parse response from aamarpay",
            "exception": str(e),
            "raw_response": getattr(r, 'text', 'No response')
        }, status=500)

    if 'payment_url' in data:
        PaymentTransaction.objects.create(
            user_profile=user.profile,
            transaction_id=transaction_id,
            amount=amount,
            status=PaymentTransaction.STATUS_INITIATED,
            gateway_response=data
        )
        return Response({"payment_url": data["payment_url"]})

    return Response({
        "error": "Payment initiation failed",
        "details": data
    }, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_transactions(request):
    profile = request.user.profile
    transactions = profile.transactions.all()
    serializer = PaymentTransactionSerializer(transactions, many=True)
    return Response(serializer.data)

@api_view(['GET', 'POST'])
@csrf_exempt
def payment_success(request):
    transaction_id = request.POST.get('mer_txnid') # 1. Check POST
    method = 'POST'

    if not transaction_id: #check GET (browser redirect)
        transaction_id = request.GET.get('mer_txnid')
        method = 'GET'

    print("Payment Success called via", method, "| transaction_id =", transaction_id)

    if not transaction_id:
        return Response({"error": "Missing transaction ID"}, status=400)
    
    # Fetch payment from DB
    payment = PaymentTransaction.objects.filter(transaction_id=transaction_id).first()
    if not payment:
        return Response({"error": "Transaction not found"}, status=404)
    
    verify_url = "https://sandbox.aamarpay.com/api/v1/trxcheck/request.php"
    params = {
        "request_id": transaction_id,
        "store_id": settings.STORE_ID,
        "signature_key": settings.SIGNATURE_KEY,
        "type": "json"
    }
    try:
        r = requests.get(verify_url, params=params)
        result = r.json()
    except Exception as e:
        return Response({"error": "Verification failed", "details": str(e)}, status=500)
    
    if result.get("pay_status") == "Successful":
        payment.status = PaymentTransaction.STATUS_SUCCESS
        payment.gateway_response = result
        payment.save()
        return Response({"message": "Payment verified and successful"})
    else:
        payment.status = PaymentTransaction.STATUS_FAILED 
        payment.gateway_response = result
        payment.save()
        return Response({"error": "Payment verification failed", "data": result}, status=400)


@api_view(['GET', 'POST'])
def payment_failed(request):
    transaction_id = request.GET.get("mer_txnid")
    payment = PaymentTransaction.objects.filter(transaction_id=transaction_id).first()
    
    if payment:
        payment.status = PaymentTransaction.STATUS_FAILED
        payment.save()
        return Response({"message": "Payment failed"})
    
    return Response({"error": "Transaction not found"}, status=404)


@api_view(['GET'])
def payment_cancelled(request):
    transaction_id = request.GET.get("mer_txnid")
    payment = PaymentTransaction.objects.filter(transaction_id=transaction_id).first()
    
    if payment:
        payment.status = PaymentTransaction.STATUS_FAILED
        payment.save()
        return Response({"message": "Payment cancelled"})
    
    return Response({"error": "Transaction not found"}, status=404)

@login_required
def transaction_history_view(request):
    transactions = request.user.profile.transactions.all().order_by('-timestamp')
    context = {
        'transactions': transactions,
    }
    return render(request, 'payments/transactions.html', context)