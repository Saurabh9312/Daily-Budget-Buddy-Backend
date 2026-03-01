from rest_framework import viewsets, generics
from rest_framework.permissions import IsAuthenticated, AllowAny
from django.contrib.auth.models import User
from rest_framework.exceptions import PermissionDenied
from .models import BankAccount, Transaction, UserProfile
from .serializers import BankAccountSerializer, TransactionSerializer, RegisterSerializer, UserProfileSerializer

class UserProfileView(generics.RetrieveUpdateAPIView):
    serializer_class = UserProfileSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        profile, created = UserProfile.objects.get_or_create(user=self.request.user)
        return profile

class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

class BankAccountViewSet(viewsets.ModelViewSet):
    serializer_class = BankAccountSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return BankAccount.objects.filter(user=self.request.user).order_by('-created_at')

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response

class TransactionViewSet(viewsets.ModelViewSet):
    serializer_class = TransactionSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Transaction.objects.filter(user=self.request.user).order_by('-date', '-created_at')

    def list(self, request, *args, **kwargs):
        queryset = self.filter_queryset(self.get_queryset())
        
        tx_type = request.query_params.get('type')
        account_id = request.query_params.get('accountId')
        
        if tx_type and tx_type != 'all':
            queryset = queryset.filter(type=tx_type)
        if account_id and account_id != 'all':
            queryset = queryset.filter(account_id=account_id)

        page = request.query_params.get('page')
        if page is not None:
            page_size = int(request.query_params.get('limit', 5))
            paginator = PageNumberPagination()
            paginator.page_size = page_size
            paginated_queryset = paginator.paginate_queryset(queryset, request)
            serializer = self.get_serializer(paginated_queryset, many=True)
            return paginator.get_paginated_response(serializer.data)

        serializer = self.get_serializer(queryset, many=True)
        return Response(serializer.data)

    def perform_create(self, serializer):
        account = serializer.validated_data['account']
        if account.user != self.request.user:
            raise PermissionDenied("You do not own this account.")
        serializer.save(user=self.request.user)
