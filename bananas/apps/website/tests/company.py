# -*- coding: utf-8; mode: django -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.test import Client, WithTestDataSeed
from website.models import Avatar, Company, Vacancy


class TestCompanyActions(TestCase):
    __metaclass__ = WithTestDataSeed

    def setUp(self):
        self.client = Client()
        self.user = self.client.login_as()
        self.avatar = any_model(
            Avatar, owner=self.user,
            today=0, hours_spent=0,
            health=50)
        self.company = any_model(Company, owner=self.avatar)
        
        self.company_url = reverse('company_index', kwargs={'avatar_pk':self.avatar.pk, 'company_pk':self.company.pk})

    def test_create_vacancy_succed(self):
        self.client.post(self.company_url, {'action':'create_vacancy', 'salary_per_hour':'1'})

        self.assertEqual(1, Vacancy.objects.filter(company=self.company).count())

        vacancy = Vacancy.objects.get(company=self.company)
        self.assertEqual(1, vacancy.salary_per_hour)

    def test_delete_vacancy_succed(self):
        bid = any_model(Vacancy, company=self.company)
        self.client.post(self.company_url, {'action':'delete_vacancy', 'vacancy_pk':'%s' % bid.pk})
        self.assertEqual(0, Vacancy.objects.count())

