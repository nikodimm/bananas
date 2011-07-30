# -*- coding: utf-8; mode: django -*-
from django.db import models
from django.contrib.auth.models import User

# activate livesettings
from website import config 


class ToManyHoursException(Exception):
    """
    Raise, when user truies to sent more that 24 hours a day
    """


class Avatar(models.Model):
    owner = models.ForeignKey(User)
    name = models.CharField(max_length=50)

    age = models.PositiveIntegerField(default=0)
    health = models.PositiveIntegerField(default=100)

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
