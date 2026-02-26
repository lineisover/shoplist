from django.urls import path

from . import views
from .views import register

app_name = 'account'

urlpatterns = [
    path('<int:user_id>/', views.profile, name='profile'),
    path('register/', register, name='register'),
]
