# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.contrib.auth.models import User

# activate livesettings
from website import config 


class ToManyHoursException(Exception):
    """
    Raise, when user truies to sent more that 24 hours a day
    """

class INVENTORY_TYPE:
    BANANAS = 'BANANAS'

INVENTORY_TYPE_CHOICES = ((INVENTORY_TYPE.BANANAS, 'Bananas'), )


class Avatar(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)

    age = models.PositiveIntegerField(default=0)
    health = models.PositiveIntegerField(default=100)
    happines = models.PositiveIntegerField(default=1000)
    
    today = models.PositiveIntegerField(default=0)
    hours_spent = models.PositiveIntegerField(default=0)

    def spent_hours(self, hours):
        """
        Tries to find free hours during day
        """
        if self.today < config.CURRENT_DAY.value:
            self.today = config.CURRENT_DAY.value
            self.hours_spent = 0

        if self.hours_spent + hours > 24:
            raise ToManyHoursException()

        self.hours_spent += hours

    def adjust_health(self, health_points):
        self.health += round(health_points)
        if self.health < 0:
            self.health = 0
        elif self.health > 100:
            self.health = 100

    def adjust_happines(self, happines_points):
        """
        There is no upper bound for happines
        """
        self.happines += round(happines_points)
        if self.happines < 0:
            self.happines = 0
            self.adjust_health(-self.health*0.1)

    def get_inventory_item(self, item_type):
        item, _ = InventoryItem.objects.get_or_create(owner=self, item_type=item_type)
        return item


class InventoryItem(models.Model):
    owner = models.ForeignKey(Avatar)
    item_type = models.CharField(choices=INVENTORY_TYPE_CHOICES, max_length=50)
    quantity = models.PositiveIntegerField(default=0)

    class Meta:
        unique_together = ('owner', 'item_type')
