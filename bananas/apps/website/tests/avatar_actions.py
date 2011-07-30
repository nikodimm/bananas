# -*- coding: utf-8; mode: django -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.test import Client, WithTestDataSeed
from website.models import Avatar

class TestAvatarActions(TestCase):
    __metaclass__ = WithTestDataSeed
    fixtures = ['default_users.json']

    def setUp(self):
        self.client = Client()
        self.user = self.client.login_as()
        self.avatar = any_model(
            Avatar, owner=self.user,
            today=0, hours_spent=0,
            health=50)
        self.avatar_url = reverse('avatar_index', kwargs={'pk':self.avatar.pk})

    def test_sleep_action_restore_health_points(self):
        initial_health = self.avatar.health
        self.client.post(self.avatar_url, {'action' : 'sleep'})
        new_health = Avatar.objects.get(pk=self.avatar.pk).health
        self.assertTrue(initial_health < new_health)
                         
