from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('checkout/', views.LockerListView.as_view(), name='checkout'),
    path('checkout/<int:locker_id>/', views.DispenseView.as_view(), name='dispense'),
    path('return/<int:locker_id>/', views.ReturnView.as_view(), name='return'),
    path('closing_doors/', views.ReturnView.as_view(), name='close')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)