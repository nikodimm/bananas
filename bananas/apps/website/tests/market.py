# -*- coding: utf-8; mode: django -*-
from django.core.urlresolvers import reverse
from django.test import TestCase
from django_any import any_model
from django_any.test import Client, WithTestDataSeed
from website.models import Avatar, Market, Bid, InventoryItem, INVENTORY_TYPE
from website.tasks import process_market


class TestBidProcessing(TestCase):
    def setUp(self):
        self.market = any_model(Market, buy_item_type=INVENTORY_TYPE.DUBLONS, sell_item_type=INVENTORY_TYPE.BANANAS)

    def test_no_bids_processing_success(self):
        process_market(self.market.id)

    def test_process_bids_success(self):
        bid1 = any_model(Bid, direction=Bid.TYPE.SELL, market=self.market, quantity=10, rate=2)
        any_model(InventoryItem, owner=bid1.owner, quantity=bid1.quantity, item_type=self.market.sell_item_type)

        bid2 = any_model(Bid, direction=Bid.TYPE.BUY, market=self.market, quantity=10, rate=2)
        any_model(InventoryItem, owner=bid2.owner, quantity=bid2.quantity*bid2.rate, item_type=self.market.buy_item_type)

        process_market(self.market.id)

        self.assertEqual(0, Bid.objects.count())

        self.assertEqual(20, bid1.owner.get_inventory_item(item_type=self.market.buy_item_type).quantity)
        self.assertEqual(10, bid2.owner.get_inventory_item(item_type=self.market.sell_item_type).quantity)

    def test_process_partial_bids_success(self):
        bid1 = any_model(Bid, direction=Bid.TYPE.SELL, market=self.market, quantity=5, rate=2)
        any_model(InventoryItem, owner=bid1.owner, quantity=bid1.quantity, item_type=self.market.sell_item_type)

        bid2 = any_model(Bid, direction=Bid.TYPE.SELL, market=self.market, quantity=5, rate=2)
        any_model(InventoryItem, owner=bid2.owner, quantity=bid2.quantity, item_type=self.market.sell_item_type)

        bid3 = any_model(Bid, direction=Bid.TYPE.BUY, market=self.market, quantity=10, rate=2)
        any_model(InventoryItem, owner=bid3.owner, quantity=bid3.quantity*bid3.rate, item_type=self.market.buy_item_type)

        process_market(self.market.id)

        self.assertEqual(0, Bid.objects.count())

    def test_process_partial_bids_with_rest_success(self):
        bid1 = any_model(Bid, direction=Bid.TYPE.SELL, market=self.market, quantity=5, rate=2)
        any_model(InventoryItem, owner=bid1.owner, quantity=bid1.quantity, item_type=self.market.sell_item_type)

        bid2 = any_model(Bid, direction=Bid.TYPE.SELL, market=self.market, quantity=7, rate=2)
        any_model(InventoryItem, owner=bid2.owner, quantity=bid2.quantity, item_type=self.market.sell_item_type)

        bid3 = any_model(Bid, direction=Bid.TYPE.BUY, market=self.market, quantity=10, rate=2)
        any_model(InventoryItem, owner=bid3.owner, quantity=bid3.quantity*bid3.rate, item_type=self.market.buy_item_type)

        process_market(self.market.id)

        self.assertEqual(1, Bid.objects.count())
        self.assertEqual(2, Bid.objects.all()[0].quantity)


class TestBidActions(TestCase):
    __metaclass__ = WithTestDataSeed

    def setUp(self):
        self.client = Client()
        self.user = self.client.login_as()
        self.avatar = any_model(
            Avatar, owner=self.user,
            today=0, hours_spent=0,
            health=50)
        self.market = any_model(
            Market, buy_item_type=INVENTORY_TYPE.DUBLONS,
            sell_item_type=INVENTORY_TYPE.BANANAS)
        
        self.market_url = reverse('market_index', kwargs={'avatar_pk':self.avatar.pk, 'market_pk':self.market.pk})

    def test_create_bid_succed(self):
        self.client.post(self.market_url, {'action':'create_bid', 'quantity':'10', 'rate':'200', 'direction':'SELL'})

        self.assertEqual(1, Bid.objects.filter(owner=self.avatar).count())

        bid = Bid.objects.get(owner=self.avatar)
        self.assertEqual(10, bid.quantity)
        self.assertEqual(self.market, bid.market)

    def test_delete_bid_succed(self):
        bid = any_model(Bid, owner=self.avatar, market=self.market)
        self.client.post(self.market_url, {'action':'delete_bid', 'bid_pk':'%s' % bid.pk})

        self.assertEqual(0, Bid.objects.filter(owner=self.avatar).count())
