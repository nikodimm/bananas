# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.contrib.auth.models import User
from social_auth.signals import socialauth_registered

# activate livesettings
from website import config 


class ToManyHoursException(Exception):
    """
    Raise, when user truies to sent more that 24 hours a day
    """

class INVENTORY_TYPE:
    BANANAS = 'BANANAS'
    BANANA_PIES = 'BANANA_PIES'
    DUBLONS = 'DUBLONS'
    GOLD = 'GOLD'

INVENTORY_TYPE_CHOICES = (
    (INVENTORY_TYPE.BANANAS, 'Bananas'),
    (INVENTORY_TYPE.BANANA_PIES, 'Banana pies'),
    (INVENTORY_TYPE.DUBLONS, 'Dublons'),
    (INVENTORY_TYPE.GOLD, 'Gold'),
)


class Avatar(models.Model):
    """
    Since we going to alllow avatars to die, let users
    to have more than one game character
    """
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
    """
    Money or other things belongs to avatar
    """
    owner = models.ForeignKey(Avatar)
    item_type = models.CharField(choices=INVENTORY_TYPE_CHOICES, max_length=50)
    quantity = models.DecimalField(default=0, decimal_places=2, max_digits=15)

    class Meta:
        unique_together = ('owner', 'item_type')


class Market(models.Model):
    """
    The place where evrybody could sells and buys anithing
    """
    name = models.CharField(max_length=50)
    sell_item_type = models.CharField(choices=INVENTORY_TYPE_CHOICES, max_length=50)
    buy_item_type = models.CharField(choices=INVENTORY_TYPE_CHOICES, max_length=50)


class Bid(models.Model):
    """
    The users bid for the market
    """
    class TYPE:
        SELL = 'SELL'
        BUY = 'BUY'
    TYPE_CHOICES = ((TYPE.SELL, 'Sell'),
                    (TYPE.BUY, 'Buy'))

    created = models.DateTimeField(auto_now_add=True)

    owner = models.ForeignKey(Avatar)
    marker = models.ForeignKey(Market)
    quantity = models.DecimalField(decimal_places=2, max_digits=15)
    rate = models.DecimalField(decimal_places=2, max_digits=15)
    direction = models.CharField(max_length=50, choices=TYPE_CHOICES)

    
def new_users_handler(sender, user, response, details, **kwargs):
    """
    Each users gets one inital avatar for play
    """
    Avatar.objects.get_or_create(owner=user, name=user.username)
    return False

socialauth_registered.connect(new_users_handler, sender=None)
