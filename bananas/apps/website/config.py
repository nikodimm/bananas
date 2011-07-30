# -*- coding: utf-8; mode: django -*-
from livesettings import config_register, ConfigurationGroup, \
     PositiveIntegerValue

WEBSITE_GROUP = ConfigurationGroup('website','Global website settings')

CURRENT_DAY = config_register(
    PositiveIntegerValue(
        WEBSITE_GROUP, 'current_day',
        description = 'Current game day', default=1))
