from django.urls import path
from django.conf import settings
from django.conf.urls.static import static

from . import views

urlpatterns = [
    path('', views.IndexView.as_view(), name='index'),
    path('checkout/', views.LockerListView.as_view(), name='checkout'),
    path('checkout/<int:locker_id>/dispense', views.DispenseView.as_view(), name='dispense'),
    path('checkout/<int:locker_id>/return', views.DispenseView.as_view(), name='return')
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)