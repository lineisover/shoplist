from django.urls import path

from . import views
from .views import register

app_name = 'account'

urlpatterns = [
    path('<int:user_id>/', views.profile, name='profile'),
    path('email/', views.get_email, name='get_email'),
    path('email-form/', views.get_email_form, name='get_email_form'),
    path('email-change/', views.change_email, name='change_email'),
    path('register/', register, name='register'),
]
