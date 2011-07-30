# -*- coding: utf-8; mode: django -*-
from django import forms
from website.models import Bid


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('quantity', 'rate', 'direction')
