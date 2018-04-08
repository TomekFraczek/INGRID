from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('checkout/', views.LockerListView.as_view(), name='checkout'),
]