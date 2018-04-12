from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView

from .forms import IndexForm
from .models import Locker
# from .control import doors_open
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


class LockerListView(ListView):

    template_name = 'checkout.html'
    model = Locker


class DispenseView(DetailView):

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'dispense.html'

    def get(self, request, *args, **kwargs):
        # Locker.lock.open()
        return super(DispenseView, self).get(request, *args, **kwargs)


class ReturnView(DetailView):

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'return.html'


class CloseDoorView(DetailView):

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'return.html'

    def dispatch(self, request, *args, **kwargs):
        # doors_open.wait_for_inactive()  # According to docs should be .wait_for_release() ?
        return super(CloseDoorView, self).dispatch(request, *args, **kwargs)



