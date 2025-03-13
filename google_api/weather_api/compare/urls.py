from django.urls import path
from . import views
urlpatterns = [
    path('graph/',views.compare_cities.as_view(),name='compare_cities'),
    path('pie/',views.pie_chart.as_view(),name='compare_cities'),
    path('tempgraph/',views.temp_graph.as_view(),name='temp_graph'),
    
]
