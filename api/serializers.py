from rest_framework import serializers
from django.contrib.auth.models import User
from .models import BankAccount, Transaction, UserProfile

class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True, style={'input_type': 'password'})

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            email=validated_data.get('email', ''),
            password=validated_data['password']
        )
        UserProfile.objects.create(user=user)
        return user

class UserProfileSerializer(serializers.ModelSerializer):
    username = serializers.CharField(source='user.username', read_only=True)
    email = serializers.EmailField(source='user.email', read_only=True)

    class Meta:
        model = UserProfile
        fields = ['username', 'email', 'name', 'dob', 'profile_picture']

class BankAccountSerializer(serializers.ModelSerializer):
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = BankAccount
        fields = ['id', 'name', 'color', 'createdAt']

class TransactionSerializer(serializers.ModelSerializer):
    accountId = serializers.PrimaryKeyRelatedField(
        source='account',
        queryset=BankAccount.objects.all(),
    )
    createdAt = serializers.DateTimeField(source='created_at', read_only=True)

    class Meta:
        model = Transaction
        fields = ['id', 'type', 'amount', 'description', 'accountId', 'date', 'createdAt']
