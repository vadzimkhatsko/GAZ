from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    index,
    register_view,
    ContractView,
    create_contract,
    change_contract
)



urlpatterns = [
    path('', index),
    path('register/', register_view, name='register'),
    path('contracts/', login_required(ContractView.as_view()), name='contracts'),
    path('contracts/create_contract/', create_contract, name='create_contract'),
    path('contracts/change_contract/<contract_id>', change_contract, name='change_contract'),

]