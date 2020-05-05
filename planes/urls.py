from django.urls import path, include
from .views import (
    index,
    register_view
)


urlpatterns = [
    path('', index),
    path('register/', register_view, name='register')

]