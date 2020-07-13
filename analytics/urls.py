from django.urls import path, include
from django.contrib.auth.decorators import login_required
from .views import analytics, report_RKDZ, report_RKDZ_table, RKDZ_template, RKDZ_add
from .analytics import get_analytics_for_all_contracts, get_deviation_analysis

app_name = "analytics"


urlpatterns = [
    path('', analytics, name='analytics'),
    path('implementation_plan/', get_analytics_for_all_contracts, name='implementation_plan'),
    path('deviation_analysis/', get_deviation_analysis, name='deviation_analysis'),
    path('report_RKDZ/', report_RKDZ, name='report_RKDZ'),
    path('report_RKDZ_table/', report_RKDZ_table, name='report_RKDZ_table'),
    path('RKDZ_template/', RKDZ_template, name='RKDZ_template'),
    path('RKDZ_add/', RKDZ_add, name='RKDZ_add'),
]
