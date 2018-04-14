from django import forms


class IndexForm(forms.Form):

    rfid = forms.CharField(widget=forms.TextInput(attrs={'autofocus': 'autofocus'}))#widget=forms.HiddenInput)

    def send_email(self):
        # send email using the self.cleaned_data dictionary
        pass

