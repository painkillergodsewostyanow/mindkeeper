from django.urls import path
from .views import UserRegistrationView, UserLoginView, VerifyEmailRequiredTemplateView, VerifyEmailView

app_name = 'society'

urlpatterns = [

    path('registration/', UserRegistrationView.as_view(), name='registration'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('required_verify_email', VerifyEmailRequiredTemplateView.as_view(), name='required_verify_email'),
    path('verify_email/<uidb64>/<token>', VerifyEmailView.as_view(), name='verify_email')

]

