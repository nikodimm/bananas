# -*- coding: utf-8; mode: django -*-
from django.contrib import admin
from website.models import Avatar, InventoryItem, Market, Bid


class MarketAdmin(admin.ModelAdmin):
    list_display = ('name', 'sell_item_type', 'buy_item_type')


admin.site.register(Avatar)
admin.site.register(InventoryItem)
admin.site.register(Market, MarketAdmin)
admin.site.register(Bid)

