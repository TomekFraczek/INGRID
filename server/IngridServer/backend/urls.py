from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from server.IngridServer.backend.views import *

urlpatterns = [
                  path('', IndexView.as_view(), name='index'),
                  path('checkout/', LockerListView.as_view(), name='checkout'),
                  path('checkout/<int:locker_id>/', DispenseView.as_view(), name='dispense'),
                  path('return/<int:locker_id>/', ReturnView.as_view(), name='return'),
                  path('closing_doors/', ReturnView.as_view(), name='close')
              ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
