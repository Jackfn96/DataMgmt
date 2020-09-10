from django import forms


class ContractForm(forms.Form):
    locker_name = forms.CharField()
    myfile = forms.FileField()


class StateForm(forms.Form):
    third_party_email = forms.CharField()
    intended_purpose = forms.CharField()


class RequestForm(forms.Form):
    intended_purpose = forms.CharField()
