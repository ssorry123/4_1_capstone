from django.urls import path

from . import views

app_name = 'sg'
urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('post/', views.post, name='post'),
    path('post/results/', views.results, name='results'),
    path('post/results/save/', views.save, name='save'),
    path('<int:pk>/', views.DetailView.as_view(), name='detail'),
]