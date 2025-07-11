from django.urls import path
from .views import *

urlpatterns = [
    path('login/', LoginView.as_view(), name='login-name'),
    path('register/', RegisterView.as_view(), name='register-name'),
    path('logout/', LogoutView.as_view(), name='logout-name')

]