from django.contrib.auth import get_user_model
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.conf import settings
from invoice.models import Order
from invoice.serializers import OrderSerializer

from rest_framework.views import APIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from rest_framework_simplejwt.tokens import RefreshToken

from .serializers import (
    RegisterSerializer,
    UserProfileSerializer,
    PasswordResetRequestSerializer,
    PasswordResetConfirmSerializer,
    UserResponseSerializer
)

User = get_user_model()
  

class RegisterView(APIView):
    '''singup view'''
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)
            return Response({
                "user": UserResponseSerializer(user).data,
                "refresh": str(refresh),
                "access": str(refresh.access_token),
                "msg": "User Registered Successfully"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserProfileView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(request.user)
        user_data = serializer.data
        orders = Order.objects.filter(email = request.user.email)
        orders_serializer = OrderSerializer(orders, many=True)
        orders_data = orders_serializer.data
        context = {
            "user information ": user_data,
            "order data":orders_data
        }
        return Response(context, status=status.HTTP_200_OK)
        

    

class PasswordResetRequestView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetRequestSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.validated_data['email']
            try:
                user = User.objects.get(email__iexact=email)
            except User.DoesNotExist:
                return Response({"error": "User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)

            token = default_token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_url = f"{settings.FRONTEND_URL}/reset-password/{uid}/{token}/"

            subject = "Password Reset for Your Trendoes Account"
            message = render_to_string('users/password_reset_email.html', {
                'user': user,
                'reset_url': reset_url,
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])

            return Response({"msg": "Password reset link has been sent to your email."}, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class PasswordResetConfirmView(APIView):
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = PasswordResetConfirmSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({"msg": "Password has been reset successfully."}, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
