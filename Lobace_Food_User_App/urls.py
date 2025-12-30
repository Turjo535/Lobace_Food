
from django.urls import path
from .views import UserSignupView,EmailVerificationView,SendOtpView,ChangePasswordView,LoginView,ForgetPasswordView
urlpatterns = [
    path("signup/",UserSignupView.as_view(),name="user-signup"),
    path("verify-email/",EmailVerificationView.as_view(),name="email-verification"),
    path("send-otp/",SendOtpView.as_view(),name="send-otp"),
    path("change-password/",ChangePasswordView.as_view(),name="change-password"),
    path("login/",LoginView.as_view(),name="user-login"),
    path("forget-password/",ForgetPasswordView.as_view(),name="forget-password"),
]