from django.contrib import messages
from django.shortcuts import render
from django.shortcuts import redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from .token import send_email

from django.views import View
from django.views.generic import FormView, RedirectView, TemplateView
from django.contrib.auth import login, authenticate, logout
from accounts.forms import CustomUserCreateForm, CustomLoginCreateForm
from django.contrib.auth import get_user_model

User = get_user_model()


class RegisterFormView(FormView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("activate")
    template_name = 'accounts/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_email(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = CustomLoginCreateForm
    success_url = 'task'
    template_name = 'accounts/login.html'

    def form_valid(self, form):
        user = authenticate(username=self.request.POST['username'],
                            password=self.request.POST['password'])
        login(self.request, user)
        return super(LoginFormView, self).form_valid(form)


class LogoutFormView(View):
    def get(self, request):
        logout(request)
        return redirect(reverse('login'))


class ActivateFormView(RedirectView):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except Exception as error:
            user = None
        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return render(request, "accounts/activate_success.html")
        else:
            return render(request, "accounts/activate_invalid.html")


class CheckEmailView(TemplateView):
    template_name = 'check_email.html'


class SuccessView(TemplateView):
    template_name = 'activate_success.html'
