from django.urls import path, include
from .views import (
    index,
    register_view,
    ContractView,
)


urlpatterns = [
    path('', index),
    path('register/', register_view, name='register'),
    path('contracts/', ContractView.as_view(), name='contracts'),

]