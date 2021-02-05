from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('<int:therapist_id>', views.therapist_page, name='therapist')
]