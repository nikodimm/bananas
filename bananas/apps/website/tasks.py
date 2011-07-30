# -*- coding: utf-8; mode: django -*-
from celery.task import task
from website import config

@task
def adjust_game_clock():
    config.CURRENT_DAY.update(config.CURRENT_DAY+1)
