from django.urls import path, include

from accounts.views import RegisterFormView, LoginFormView, LogoutFormView, ActivateFormView, CheckEmailView, \
    SuccessView, InvalidView

urlpatterns = [
    path('', RegisterFormView.as_view(), name='register'),
    path('login/', LoginFormView.as_view(), name='login'),
    path('activate/<uidb64>/<token>/', ActivateFormView.as_view(), name="activate"),
    path('check-email/', CheckEmailView.as_view(), name="check_email"),
    path('activate_success/', SuccessView.as_view(), name="activate_success"),
    path('activate_invalid/', InvalidView.as_view(), name="activate_invalid"),
    path('logout/', LogoutFormView.as_view(), name='logout'),
    path('login/task/', include('task.urls'), name='task')
]
