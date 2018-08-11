import os

from django.urls import reverse
from django.views.generic import ListView, FormView, DetailView, RedirectView
from json import load
from playsound import playsound

from .convinience import is_member_rfid, is_wetsuit_rfid
from .forms import IndexForm
from .models import Locker

NO_ACTIVE_LOCKER = -1

settings = load(open(os.path.join(os.getcwd(), 'ingridbackend', 'static', 'config.json')))
active_locker = NO_ACTIVE_LOCKER


class IndexView(FormView):
    """The homepage view that waits for someone to scan a RFID tags"""

    template_name = 'index.html'
    form_class = IndexForm

    def get_success_url(self):
        form = self.get_form()
        rfid = form.data['rfid']

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

    def get_queryset(self):
        return Locker.objects.filter(should_have_suit=True)


class DispenseView(DetailView):
    """View that handles the giving out of a wetsuit"""

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'dispense.html'

    def get(self, request, *args, **kwargs):
        global active_locker
        active_locker = Locker.locker_id
        Locker.should_have_suit = False
        Locker.lock.open()
        return super(DispenseView, self).get(request, *args, **kwargs)


class ReturnView(DetailView):
    """View that handles the returning of a wetsuit"""

    model = Locker
    pk_url_kwarg = 'locker_id'
    template_name = 'return.html'

    def get(self, request, *args, **kwargs):
        global active_locker
        active_locker = Locker.locker_id
        Locker.should_have_suit = True
        Locker.lock.open()
        return super(ReturnView, self).get(request, *args, **kwargs)


class CloseDoorView(RedirectView):
    """View called upon the closing of all doors that ensures a healthy state"""

    pk_url_kwarg = 'locker_id'
    template_name = 'return.html'

    def get_redirect_url(self, *args, **kwargs):

        redirect_url = reverse('index')

        locker = Locker.objects.get(locker_id=active_locker)

        # If a locker is missing a suit, demand it back
        if locker.should_have_suit and not locker.has_suit:
            # playsound(settings['audio']['return wetsuit'])
            redirect_url = reverse('return', kwargs={'locker_id': locker.locker_id})

        # If a locker unexpectedly has a suit, set the expected status to have_suit
        if not locker.should_have_suit and locker.has_suit:
            locker.should_have_suit = True

        # Clear the active locker before returning (with be set back if a locker becomes active)
        global active_locker
        active_locker = NO_ACTIVE_LOCKER

        return redirect_url
