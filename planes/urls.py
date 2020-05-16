from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import (
    index,
    register_view,
    ContractView,
    fabricate_contract,
    adding_click_to_UserActivityJournal,
    curators,
    from_js,
    edit_plane,
    add,
    plane,
)

app_name = "planes"


urlpatterns = [
    path('', plane, name='plane' ),
    path('register/', register_view, name='register'),
    path('contracts/', login_required(ContractView.as_view()), name='contracts'),
    path('contracts/create_contract/', fabricate_contract, name='create_contract'),
    path('contracts/change_contract/<contract_id>', fabricate_contract, name='change_contract'),
    path('add_click/', adding_click_to_UserActivityJournal, name='add_click'),
    path('<int:finance_cost_id>/curators/', curators, name='curators'),
    path('to_server/', from_js, name='from_js'),
    path('<int:item_id>/edit-plane', edit_plane, name='edit_plane'),
    path('<int:finance_cost_id>/add/', add, name= 'add')
]
