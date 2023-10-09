from django.contrib.auth.views import LogoutView
from django.urls import path
from .views import *

app_name = 'users'

urlpatterns = [

    path('log_reg_page', LogRegView.as_view(), name='log_reg_page'),
    path('registration/', reg_user, name='registration'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('required_verify_email', VerifyEmailRequiredTemplateView.as_view(), name='required_verify_email'),
    path('verify_email/<uidb64>/<token>', VerifyEmailView.as_view(), name='verify_email')

]

