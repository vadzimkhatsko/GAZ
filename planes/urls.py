from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    index,
    register_view,
    ContractView,
    fabricate_contract,
    adding_click_to_UserActivityJournal,
)



urlpatterns = [
    path('', index),
    path('register/', register_view, name='register'),
    path('contracts/', login_required(ContractView.as_view()), name='contracts'),
    path('contracts/create_contract/', fabricate_contract, name='create_contract'),
    path('contracts/change_contract/<contract_id>', fabricate_contract, name='change_contract'),
    path('add_click/', adding_click_to_UserActivityJournal, name='add_click'),


]