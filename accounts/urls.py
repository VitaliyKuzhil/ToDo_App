from django.urls import path

from accounts.views import RegisterFormView, LoginFormView, LogoutFormView, ActivateFormView, CheckEmailView, \
    SuccessView, InvalidView, ProfileView, UpdateProfileView

urlpatterns = [
    path('', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateFormView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('activate-success/', SuccessView.as_view(), name="activate_success"),
    path('activate-invalid/', InvalidView.as_view(), name="activate_invalid"),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('profile/', ProfileView.as_view(), name='user_profile'),
    path('update-user-profile/<int:pk>/', UpdateProfileView.as_view(), name='update_user_profile'),
]
