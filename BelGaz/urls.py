from django.contrib import admin
from django.urls import path, include
from planes.views import login_view, logout_view, index
from schema_graph.views import Schema

urlpatterns = [
    path('', login_view, name='login'),
    path('admin/', admin.site.urls),
    path('schema/', Schema.as_view()),
    path('logout/', logout_view, name='logout'),
    path('plane/', include('planes.urls', namespace='planes')),
    path('catalog/', include('catalog.urls')),
]
