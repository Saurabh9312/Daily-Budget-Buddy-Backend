from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import BankAccountViewSet, TransactionViewSet, RegisterView, UserProfileView

router = DefaultRouter()
router.register(r'accounts', BankAccountViewSet, basename='accounts')
router.register(r'transactions', TransactionViewSet, basename='transactions')

urlpatterns = [
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegisterView.as_view(), name='register'),
    path('profile/', UserProfileView.as_view(), name='user_profile'),
    path('', include(router.urls)),
]
