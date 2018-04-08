from django.shortcuts import render
from django.http import HttpResponse
from django.views.generic import ListView, FormView

from .forms import IndexForm
from .convinience import is_member_rfid, is_wetsuit_rfid


# Create your views here.
class IndexView(FormView):

    template_name = 'index.html'
    form_class = IndexForm

    def get_success_url(self):
        form = self.get_form()
        rfid = form.data['rfid']


        # TODO: make these URL's not be hardcoded
        if is_wetsuit_rfid(rfid):
            return 'ingrid/return/'
        elif is_member_rfid(rfid):
            return 'ingrid/checkout/'
        else:
            return 'ingrid/'


class WetsuitListView(ListView):
    pass
