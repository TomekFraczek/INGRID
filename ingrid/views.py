from django.shortcuts import render
from django.http import HttpResponse
from django.urls import reverse
from django.views.generic import ListView, FormView

from .forms import IndexForm
from .models import Wetsuit
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
            return reverse('return')
        elif is_member_rfid(rfid):
            return reverse('checkout')
        else:
            return reverse('index')


class WetsuitListView(ListView):

    template_name = 'checkout.html'
    model = Wetsuit

