from django.urls import path

from . import views

app_name = 'practice'
urlpatterns = [
    path('', views.indexView, name='index'),
    path('results/', views.ResultsView.as_view(), name='results'),
]