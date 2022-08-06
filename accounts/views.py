from django.contrib.auth import get_user_model
from django.contrib.auth import login, authenticate, logout
from django.shortcuts import render, redirect
from django.urls import reverse_lazy, reverse
from django.utils.encoding import force_str
from django.utils.http import urlsafe_base64_decode
from django.contrib.auth.tokens import default_token_generator as token_generator
from .token import send_email

from accounts.forms import CustomUserCreateForm, CustomLoginCreateForm, CustomUserChangeForm
from django.views import View
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import FormView, TemplateView, UpdateView

from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from .serializers import CustomUserSerializer
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

User = get_user_model()


class RegisterFormView(FormView):
    form_class = CustomUserCreateForm
    success_url = reverse_lazy("check_email")
    template_name = 'accounts/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect("task:list_task")
        return super(RegisterFormView, self).get(request, *args, **kwargs)

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = False
        user.save()
        send_email(self.request, user)
        return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
    form_class = CustomLoginCreateForm
    success_url = reverse_lazy('task:list_task')
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


class ActivateFormView(View):

    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None
        if user and token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            return redirect(reverse("activate_success"))

        return redirect(reverse("activate_invalid"))


class CheckEmailView(TemplateView):
    template_name = 'accounts/check_email.html'


class SuccessView(TemplateView):
    template_name = 'accounts/activate_success.html'


class InvalidView(TemplateView):
    template_name = 'accounts/activate_invalid.html'


class ProfileView(View):

    def get(self, request):
        user = self.request.user
        context = {'user': user}
        return render(request, 'accounts/user_profile.html', context=context)


class UpdateProfileView(LoginRequiredMixin, UpdateView):
    model = User
    form_class = CustomUserChangeForm
    template_name = 'accounts/update_user_profile.html'
    template_name_suffix = '_update_user_profile'


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)

        return Response({
            'token': token.key,
            'user_id': user.pk,
            'email': user.email})


class CustomUserApiView(ModelViewSet):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'put', 'patch']

    def perform_create(self, serializer):
        if self.request.user.is_authenticated:
            serializer.save(**{'email': self.request.user.email})

    def get_queryset(self):
        email = self.request.user.email
        return User.objects.filter(email=email)
