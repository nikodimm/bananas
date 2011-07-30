# -*- coding: utf-8; mode: django -*-
from django import forms
from website.models import Bid, Company, Vacancy


class BidForm(forms.ModelForm):
    class Meta:
        model = Bid
        fields = ('quantity', 'rate', 'direction')


class CompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = ('name', )


class VacancyForm(forms.ModelForm):
    class Meta:
        model = Vacancy
        fields = ('salary_per_hour', )
