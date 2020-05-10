from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    index,
    register_view,
    ContractView,
)



urlpatterns = [
    path('', index),
    path('register/', register_view, name='register'),
    path('contracts/', login_required(ContractView.as_view()), name='contracts'),

]