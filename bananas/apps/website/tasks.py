# -*- coding: utf-8; mode: django -*-
from django.db import transaction
from celery.task import task
from website import config
from website.models import Bid, NotEnoughQuantity


@task
def adjust_game_clock():
    config.CURRENT_DAY.update(config.CURRENT_DAY+1)


@task
@transaction.commit_manually
def process_market(market_id):
    """
    Takes first 50 sell bids, and all buy bids with
    rate less thant 5'th sell bids, and performs the deal
    """
    sell_bids = list(Bid.objects.filter(market__id=market_id, direction=Bid.TYPE.SELL).order_by('-rate', '-created')[:100])

    if not sell_bids:
        return

    process_rate = sell_bids[-5:][0].rate
    buy_bids = Bid.objects.filter(market__id=market_id, direction=Bid.TYPE.BUY, rate__lte=process_rate).order_by('-created')[:100]


    for buy_bid in buy_bids:
        try:
            while buy_bid.quantity > 0 and buy_bid.rate <= sell_bids[-1].rate:
                affected_bids = [buy_bid]
                sell_bid = sell_bids[-1]
                
                deal_quantity = min(sell_bid.quantity, buy_bid.quantity)

                buy_bid.process(deal_quantity, sell_bid.rate)
                sell_bid.process(deal_quantity, sell_bid.rate)

                affected_bids.append(sell_bid)
                sell_bids.pop()

                for bid in affected_bids:
                    if bid.quantity == 0:
                        bid.delete()

                if not sell_bids:
                    break

        except NotEnoughQuantity, e:
            transaction.rollback()
            e.bid.delete()
            transaction.commit()
        else:
            transaction.commit()
