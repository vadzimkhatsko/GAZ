from django.shortcuts import render
from planes.models import (
    FinanceCosts,
    ActivityForm,
    Curator,
    ContractType,
    ContractMode,
    PurchaseType,
    StateASEZ,
    Counterpart,
    ContractStatus,
    UserTypes,
    NumberPZTRU,
)
from . import forms
from django.forms import modelformset_factory

# Create your views here.
def index(request):
    context = {}
    return render(request, 'catalog/index.html', context)

def catalog_funding(request):
    CatalogFormset = modelformset_factory(FinanceCosts, form=forms.CatalogFinanceCostsForm)
    formset = CatalogFormset()
    title = 'Статьи финансирования'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_activityform(request):
    CatalogFormset = modelformset_factory(ActivityForm, form=forms.CatalogActivityFormForm)
    formset = CatalogFormset()
    title = 'Виды деятельности'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_curator(request):
    CatalogFormset = modelformset_factory(Curator, form=forms.CatalogCuratorForm)
    formset = CatalogFormset()
    title = 'Кураторы'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_contracttype(request):
    CatalogFormset = modelformset_factory(ContractType, form=forms.CatalogContractTypeForm)
    formset = CatalogFormset()
    title = 'Типы договора'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_contractmode(request):
    CatalogFormset = modelformset_factory(ContractMode, form=forms.CatalogContractModeForm)
    formset = CatalogFormset()
    title = 'Виды договора'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_purchasetype(request):
    CatalogFormset = modelformset_factory(PurchaseType, form=forms.CatalogPurchaseTypeForm)
    formset = CatalogFormset()
    title = 'Типы закупки'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_stateasez(request):
    CatalogFormset = modelformset_factory(StateASEZ, form=forms.CatalogStateASEZForm)
    formset = CatalogFormset()
    title = 'Состояния АСЭЗ'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_counterpart(request):
    CatalogFormset = modelformset_factory(Counterpart, form=forms.CatalogCounterpartForm)
    formset = CatalogFormset()
    title = 'Контрагенты'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_contractstatus(request):
    CatalogFormset = modelformset_factory(ContractStatus, form=forms.CatalogContractStatusForm)
    formset = CatalogFormset()
    title = 'Статусы договора'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_usertypes(request):
    CatalogFormset = modelformset_factory(UserTypes, form=forms.CatalogUserTypesForm)
    formset = CatalogFormset()
    title = 'Типы пользователя'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_numberpztru(request):
    CatalogFormset = modelformset_factory(NumberPZTRU, form=forms.CatalogNumberPZTRUForm)
    formset = CatalogFormset()
    title = '№ пункта положения о закупках'
    context = {'formset': formset, 'title': title}
    return render(request, 'catalog/article.html', context)

def catalog_report(request):
    pass
