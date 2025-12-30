from django.shortcuts import render
from django.http import JsonResponse
from rest_framework.views import APIView
from rest_framework import status
import pytz
from rest_framework.permissions import IsAuthenticated
from datetime import datetime
from rest_framework.response import Response
from .serializer import UserSignupSerializer
from .models import CustomUser
from .email import send_verification_code
from datetime import datetime, timedelta
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)

# Create your views here.

class UserSignupView(APIView):
    def post(self,request):
        serializer=UserSignupSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email=serializer.data.get('email')
            user=CustomUser.objects.get(email=email)

            send_verification_code(user)

            return Response({"message":"User Created Successfully.","message":"Verification code sent to your email."},status=status.HTTP_201_CREATED)
        return Response({"message":serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
    
class EmailVerificationView(APIView):
    def post(self,request):
        email=request.data.get('email')
        otp=request.data.get('otp_code')
        try:
            user=CustomUser.objects.get(email=email)
            if user.otp_code == otp and user.otp_created + timedelta(minutes=5) > datetime.now(pytz.utc):
                user.is_active = True
                user.otp_code = None
                user.otp_created = None
                user.save()
                return Response({"message":"Email verified successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)
        except CustomUser.DoesNotExist:
            return Response({"message":"User with this email does not exist."},status=status.HTTP_404_NOT_FOUND)


class SendOtpView(APIView):
    def post(self, request):
        email=request.data.get('email')
        try:
            user=CustomUser.objects.get(email=email)
            send_verification_code(user)
            return Response({"message":"Verification code sent to your email"},status=status.HTTP_200_OK)
    
        except CustomUser.DoesNotExist:
            return Response({"message":"User with this email does not exist"},status=status.HTTP_404_NOT_FOUND)
        
class ChangePasswordView(APIView):
    permission_classes=[IsAuthenticated]
    def post(self,request):
        user=request.user
        current_password=request.data.get('current_password')
        new_password=request.data.get('new_password')
        confirm_password=request.data.get('confirm_password')
        try:
            if not user.check_password(current_password):
                return Response({"message":"Current password is incorrect."},status=status.HTTP_400_BAD_REQUEST)
            if new_password != confirm_password:
                return Response({"message":"New password and confirm password do not match."},status=status.HTTP_400_BAD_REQUEST)   
            user.set_password(new_password)
            user.save()
            return Response({"message":"Password changed successfully."},status=status.HTTP_200_OK)
        except Exception as e:
            return Response({"message":str(e)},status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
        try:
            user = CustomUser.objects.get(email=email)
            if user.check_password(password):
                refresh = RefreshToken.for_user(user)
                return Response({
                    'message':'Login successful.',
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }, status=status.HTTP_200_OK)
            else:
                return Response({"message":"Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        except CustomUser.DoesNotExist:
            return Response({"message":"User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)


class ForgetPasswordView(APIView):
    def post(self, request):
        email = request.data.get('email')
        otp=request.data.get('otp_code')
        new_password=request.data.get('new_password')
        confirm_password=request.data.get('confirm_password')
        try:
            user = CustomUser.objects.get(email=email)
            if new_password != confirm_password:
                return Response({"message":"New password and confirm password do not match."},status=status.HTTP_400_BAD_REQUEST)
            if user.otp_code != otp or user.otp_created + timedelta(minutes=5) < datetime.now(pytz.utc):
                return Response({"message":"Invalid or expired OTP."}, status=status.HTTP_400_BAD_REQUEST)   
            user.set_password(new_password)
            user.otp_code = None
            user.otp_created = None
            user.save()
            return Response({"message":"Password reset successfully."},status=status.HTTP_200_OK)
        except CustomUser.DoesNotExist:
            return Response({"message":"User with this email does not exist."}, status=status.HTTP_404_NOT_FOUND)
        