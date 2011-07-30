# -*- coding: utf-8; mode: django -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.test import Client, WithTestDataSeed
from website.models import Avatar, Company, Vacancy, CompanyWorker, \
     InventoryItem, INVENTORY_TYPE


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

    def test_work_with_enough_company_money_succeed(self):
        CompanyWorker.objects.create(worker=self.avatar, company=self.company, salary_per_hour=1)
        any_model(InventoryItem, owner=self.avatar, quantity=10, item_type=INVENTORY_TYPE.DUBLONS)        

        initial_health = self.avatar.health
        self.client.post(self.company_url, {'action':'work'})
        new_health = Avatar.objects.get(pk=self.avatar.pk).health
        self.assertTrue(initial_health > new_health)
