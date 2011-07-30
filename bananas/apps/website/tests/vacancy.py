# -*- coding: utf-8; mode: django -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.test import Client, WithTestDataSeed
from website.models import Avatar, Vacancy

class TestVacancyActions(TestCase):
    __metaclass__ = WithTestDataSeed

    def setUp(self):
        self.client = Client()
        self.user = self.client.login_as()
        self.avatar = any_model(
            Avatar, owner=self.user,
            today=0, hours_spent=0,
            health=50)
        self.vacancy_url = reverse('vacancy_index', kwargs={'avatar_pk':self.avatar.pk})


    def test_accept_vacancy_succed(self):
        vacancy = any_model(Vacancy)

        self.client.post(self.vacancy_url, {'action':'accept_vacancy', 'vacancy_pk' : '%s' % vacancy.pk })

        self.assertEqual(0, Vacancy.objects.count())
