from django.urls import path
from users.api.views import UserSignUpView, UserLoginView, SendSignUpEmailView, VerifyEmailCodeView, \
    SendPasswordResetCodeView, PasswordResetView, PublisherSignUpView, PublisherImageUploadView, \
    PublisherDetailsUpdateView


urlpatterns = [
    path("user/signup", UserSignUpView.as_view(), name="user-signup"),
    path("login", UserLoginView.as_view(), name="login"),
    path("send-signup-email", SendSignUpEmailView.as_view(), name="send-email"),
    path("verify-email-code", VerifyEmailCodeView.as_view(), name="verify-code-email"),
    path("send-resetpassword-code", SendPasswordResetCodeView.as_view(), name="password-reset-code"),
    path("reset-password", PasswordResetView.as_view(), name="reset-password"),
    path("publisher/signup", PublisherSignUpView.as_view(), name="publisher-signup"),
    path("publisher/signup-1", PublisherDetailsUpdateView.as_view(), name="publisher-detail"),
    path("publisher/signup-2", PublisherImageUploadView.as_view(), name="publisher-file-upload"),
]
