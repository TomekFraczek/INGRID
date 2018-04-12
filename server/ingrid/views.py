import os

from json import load
from playsound import playsound
from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView, RedirectView

from .forms import IndexForm
from .models import Locker
from .convinience import is_member_rfid, is_wetsuit_rfid

settings = load(os.path.join(os.getcwd(), 'ingrid', 'static', 'config.json'))


class IndexView(FormView):
    """The homepage view that waits for someone to scan a RFID tags"""

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
    """View that displays all the wetsuits available for checkout"""

    template_name = 'checkout.html'
    model = Locker


class DispenseView(DetailView):
    """View that handles the giving out of a wetsuit"""

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'dispense.html'

    def get(self, request, *args, **kwargs):
        Locker.should_have_suit = False
        Locker.lock.open()
        return super(DispenseView, self).get(request, *args, **kwargs)


class ReturnView(DetailView):
    """View that handles the returning of a wetsuit"""

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'return.html'

    def get(self, request, *args, **kwargs):
        Locker.should_have_suit = True
        Locker.lock.open()
        return super(ReturnView, self).get(request, *args, **kwargs)


class CloseDoorView(RedirectView):
    """View called upon the closing of all doors that ensures a healthy state"""

    pk_url_kwarg = 'locker_id'
    template_name = 'return.html'

    def get_redirect_url(self, *args, **kwargs):

        redirect_url = reverse('index')

        for locker in Locker.objects.all():

            # If a locker is missing a suit, demand it back
            if locker.should_have_suit and not locker.has_suit:
                playsound(settings['audio']['return wetsuit'])
                redirect_url = reverse('return', kwargs={'locker_id': locker.locker_id})

            # If a locker unexpectedly has a suit, set the expected status to have_suit
            if not locker.should_have_suit and locker.has_suit:
                locker.should_have_suit = True

        return redirect_url





