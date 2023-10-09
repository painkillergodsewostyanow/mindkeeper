from django.contrib.auth import authenticate, login
from .forms import AuthenticationForm
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import reverse_lazy
from django.utils.http import urlsafe_base64_decode
from django.views.generic import TemplateView

from .forms import UserCreationForm
from django.shortcuts import render, redirect, get_object_or_404
from django.views import View
from email_app.tasks import send_verify_email
from .models import User


class LogRegView(View):
    template_name = 'log_reg_page.html'
    def get(self, request):
        log_form = AuthenticationForm()
        reg_form = UserCreationForm()
        return render(request, self.template_name, {'log_form': log_form, 'reg_form': reg_form})

# Create your views here.
class UserRegistrationView(View):
    template_name = 'users/registration.html'

    def get(self, request):
        return render(request, self.template_name, {'form': UserCreationForm()})

    def post(self, request):
        form = UserCreationForm(self.request.POST, self.request.FILES)
        if form.is_valid():
            form.save()
            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)
            send_verify_email.delay(user.pk)
            return redirect('users:required_verify_email')

        return render(request, self.template_name, {'form': form})


class UserLoginView(LoginView):
    template_name = 'users/login.html'
    form_class = AuthenticationForm

    def get_success_url(self):
        return reverse_lazy('main:index')


class VerifyEmailRequiredTemplateView(TemplateView):
    template_name = 'users/required_verify_email.html'


class VerifyEmailView(View):

    def get(self, request, uidb64, token):
        user = self.get_user(uidb64)
        if user and default_token_generator.check_token(user, token):
            user.is_email_verified = True
            user.save()
            login(request, user)
            return redirect('main:index')

        return render(request, 'users/invalid_token.html')

    @staticmethod
    def get_user(uidb64):
        try:
            pk = urlsafe_base64_decode(uidb64).decode()
            user = get_object_or_404(User, pk=pk)
        except (TypeError, ValueError, OverflowError, User.DoesNotExists):
            user = None
        return user