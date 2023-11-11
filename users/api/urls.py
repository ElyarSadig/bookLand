from django.urls import path
from users.api.views import UserSignUpView, UserLoginView, SendSignUpEmailView, VerifyEmailCodeView, \
    SendPasswordResetCodeView, PasswordResetView, PublisherSignUpView


urlpatterns = [
    path("auth/user/signup", UserSignUpView.as_view(), name="user-signup"),
    path("auth/login", UserLoginView.as_view(), name="login"),
    path("auth/send-signup-email", SendSignUpEmailView.as_view(), name="send-email"),
    path("auth/verify-email-code", VerifyEmailCodeView.as_view(), name="verify-code-email"),
    path("auth/send-resetpassword-code", SendPasswordResetCodeView.as_view(), name="password-reset-code"),
    path("auth/reset-password", PasswordResetView.as_view(), name="reset-password"),
    path("auth/publisher/signup", PublisherSignUpView.as_view(), name="publisher-signup"),
]
