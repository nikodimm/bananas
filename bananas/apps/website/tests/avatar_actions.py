# -*- coding: utf-8; mode: django -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.test import Client, WithTestDataSeed
from website.models import Avatar, Company, INVENTORY_TYPE

class TestAvatarActions(TestCase):
    __metaclass__ = WithTestDataSeed

    def setUp(self):
        self.client = Client()
        self.user = self.client.login_as()
        self.avatar = any_model(
            Avatar, owner=self.user,
            today=0, hours_spent=0,
            health=50)
        self.avatar_url = reverse('avatar_index', kwargs={'avatar_pk':self.avatar.pk})

    def test_sleep_action_restore_health_points(self):
        initial_health = self.avatar.health
        self.client.post(self.avatar_url, {'action' : 'sleep'})
        new_health = Avatar.objects.get(pk=self.avatar.pk).health
        self.assertTrue(initial_health < new_health)
                         
    def test_gather_bananas_extend_inventory(self):
        self.client.post(self.avatar_url, {'action' : 'gather_bananas'})
        bananas = self.avatar.get_inventory_item(INVENTORY_TYPE.BANANAS)
        self.assertEqual(1, bananas.quantity)

    def test_eathing_shoes_is_bad_for_heals(self):
        initial_health = self.avatar.health
        self.client.post(self.avatar_url, {'action' : 'eat_bananas'})
        new_health = Avatar.objects.get(pk=self.avatar.pk).health
        self.assertTrue(initial_health > new_health)

    def test_eathing_bananas_is_good_for_heals(self):
        bananas = self.avatar.get_inventory_item(INVENTORY_TYPE.BANANAS)
        bananas.quantity = 1
        bananas.save()
        
        initial_health = self.avatar.health
        self.client.post(self.avatar_url, {'action' : 'eat_bananas'})
        new_health = Avatar.objects.get(pk=self.avatar.pk).health
        self.assertTrue(initial_health < new_health)

    def test_buy_company_with_enough_gold_succeed(self):
        gold = self.avatar.get_inventory_item(INVENTORY_TYPE.GOLD)
        gold.quantity = 10
        gold.save()

        self.client.post(self.avatar_url, {'action':'buy_company', 'name' : 'TheCompany'})

        self.assertEqual(1, Company.objects.filter(owner=self.avatar).count())

        company = Company.objects.get(owner=self.avatar)
        self.assertEqual('TheCompany', company.name)
