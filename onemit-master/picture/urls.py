from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('find/', views.ResultListView.as_view(), name='result_list_view'),
    path('process', views.process, name='process'),
    path('team', views.team, name='team'),
    path('community', views.community, name='community')
    # path('find/', views.results, name='result_list_view'),
    # path('', views.get_name, name='index/get-name/'),
]