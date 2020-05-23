from django.contrib import admin
from .models import (
    Curator,
    UserTypes,
    CustomUser,
    UserActivityJournal,
    FinanceCosts,
    PurchaseType,
    ActivityForm,
    StateASEZ,
    NumberPZTRU,
    ContractStatus,
    Currency,
    ContractType,
    ContractMode,
    Counterpart,
    SumsRUR,
    SumsBYN,
    Planning,
    Contract,
    # PlanningYearFunding,
    # YearPeriod,
)

models = (
    Curator,
    # UserTypes,
    # UserSub,
    # CustomUser,
    # UserActivityJournal,
    # FinanceCosts,
    # PurchaseType,
    # ActivityForm,
    # StateASEZ,
    # NumberPZTRU,
    # ContractStatus,
    # Currency,
    # ContractType,
    # ContractMode,
    # Counterpart,
    # SumsRUR,
    # SumsBYN,
    # Planning,
    # PlanningYearFunding,
    # YearPeriod,
    UserTypes,
    CustomUser,
    UserActivityJournal,
    FinanceCosts,
    PurchaseType,
    ActivityForm,
    StateASEZ,
    NumberPZTRU,
    ContractStatus,
    Currency,
    ContractType,
    ContractMode,
    Counterpart,
    SumsRUR,
    SumsBYN,
    Planning
)


class ContractAdmin(admin.ModelAdmin):
    class Media:
        js = ("blabla.js", )


admin.site.register(Contract, ContractAdmin)


for model in models:
    admin.site.register(model)
# Register your models here.
