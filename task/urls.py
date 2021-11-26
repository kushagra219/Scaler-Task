from django.contrib import admin
from django.urls import path
# from django.conf import settings
# from django.conf.urls.static import static
from . import views

app_name = 'task'

urlpatterns = [
    path('', views.schedule_interview, name='schedule-interview'),
    path('thankyou/', views.thank_you, name='thank-you'),
]