# -*- coding: utf-8; mode: django -*-
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from website.forms import BidForm, CompanyForm, VacancyForm
from website.models import Avatar, Company, CompanyWorker, Vacancy, Market, Bid, \
     ToManyHours, INVENTORY_TYPE

def form_for_action(form_cls, action, request, **kwargs):
    if action == request.POST.get('action'):
        return form_cls(data=request.POST, **kwargs)
    else:
        return form_cls(**kwargs)


class BaseGameView(TemplateResponseMixin, View):
    def get_context_data(self, request, **kwargs):
        return {
            'avatar': get_object_or_404(Avatar, owner=request.user, pk=kwargs['avatar_pk'])
        }

    def get(self, request, *args, **kwargs):
        context = self.get_context_data(request, **kwargs)
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        if 'action' in request.POST:
            handler = getattr(
                self, 'action_%s' % request.POST['action'],
                self.http_method_not_allowed)
        else:
            handler = self.http_method_not_allowed

        context = self.get_context_data(request, **kwargs)
        try:
            context = handler(request, context, *args, **kwargs)
        except ToManyHours:
            messages.error(request, 'No more hours today, take a rest')

        return self.render_to_response(context)


class AvatarView(BaseGameView):
    template_name = 'avatar/index.html'

    def get_context_data(self, request, **kwargs):
        context = super(AvatarView, self).get_context_data(request, **kwargs)
        context['buy_company_form'] = form_for_action(CompanyForm, 'buy_company', request)
        return context

    def action_sleep(self, request, context, *args, **kwargs):
        """
        Sleep action, resotres heals poinst and make
        feels happy
        """
        context['avatar'].spent_hours(8)
        context['avatar'].adjust_health(context['avatar'].health*0.1)
        context['avatar'].save()
        return context

    def action_gather_bananas(self, request, context, *args, **kwargs):
        """
        Gather bananas into inventory
        """
        bananas = context['avatar'].get_inventory_item(INVENTORY_TYPE.BANANAS)
        bananas.quantity += 1
        bananas.save()

        context['avatar'].spent_hours(2)
        context['avatar'].adjust_health(-context['avatar'].health*0.05*bananas.quantity)

        if context['avatar'].health > 80:
            context['avatar'].adjust_happines(10)
        else:
            context['avatar'].adjust_happines(-5*bananas.quantity)
            
        context['avatar'].save()

        return context

    def action_eat_bananas(self, request, context, *args, **kwargs):
        """
        Eating bananas improove health
        """
        bananas = context['avatar'].get_inventory_item(INVENTORY_TYPE.BANANAS)

        context['avatar'].spent_hours(1)

        if bananas.quantity > 0:
            context['avatar'].adjust_health(context['avatar'].health*0.15)
            if context['avatar'].health > 50:
                context['avatar'].adjust_happines(10)
            bananas.quantity -= 1
            bananas.save()
        else:
            context['avatar'].adjust_health(-context['avatar'].health*0.01)
            messages.info(request, 'Tried to eat shoes, feels bad now')
        context['avatar'].save()            

        return context

    def action_eat_banapie(self, request, context, *args, **kwargs):
        """
        Eating bananas improove health
        """
        banana_pies = context['avatar'].get_inventory_item(INVENTORY_TYPE.BANANA_PIES)

        context['avatar'].spent_hours(1)

        if banana_pies.quantity > 0:
            context['avatar'].adjust_health(context['avatar'].health*0.15)
            if context['avatar'].health > 50:
                context['avatar'].adjust_happines(10)
            banana_pies.pies -= 1
            banana_pies.save()
        else:
            context['avatar'].adjust_health(-context['avatar'].health*0.01)
            messages.info(request, 'Tried to eat shoes, feels bad now')
        context['avatar'].save()            

        return context

    def action_sell_bananas_on_shore(self, request, context, *args, **kwargs):
        """
        Go to shore and sell bananas
        """
        bananas = context['avatar'].get_inventory_item(INVENTORY_TYPE.BANANAS)

        context['avatar'].spent_hours(4)

        if bananas.quantity > 0:
            context['avatar'].adjust_health(-context['avatar'].health*0.05*bananas.quantity)
            if context['avatar'].health > 80:
                context['avatar'].adjust_happines(5)
            else:
                context['avatar'].adjust_happines(-10*bananas.quantity)
            bananas.quantity = 0
            bananas.save()
            
            gold = context['avatar'].get_inventory_item(INVENTORY_TYPE.GOLD)
            gold.quantity += 0.05
            gold.save()
        else:
            messages.info(request, 'Tried to sell himself to slavery, nobody gets it')
            context['avatar'].adjust_health(-context['avatar'].health*0.05)
            context['avatar'].adjust_happines(-100)
            context['avatar'].save()

    def action_buy_company(self, request, context, *args, **kwargs):
        form = context['buy_company_form']
        if form.is_valid():
            gold = context['avatar'].get_inventory_item(INVENTORY_TYPE.GOLD)
            if gold.quantity >= 5:
                company = form.save(commit=False)
                company.owner = context['avatar']
                company.save()
            else:
                messages.info(request, 'They laugh at my hole-ridden suite!')
                context['avatar'].adjust_happines(-10)
                context['avatar'].save()
        else:
            messages.info(request, 'Oh, shi, please input correct values')


class MarketView(BaseGameView):
    template_name = 'market/index.html'

    def get_context_data(self, request, **kwargs):
        context = super(MarketView, self).get_context_data(request, **kwargs)
        context['market'] = Market.objects.get(pk=kwargs['market_pk'])
        context['buy_bids'] = Bid.objects.filter(market=context['market'], direction=Bid.TYPE.BUY).order_by('-rate', '-created')[:50]
        context['sell_bids'] = Bid.objects.filter(market=context['market'], direction=Bid.TYPE.SELL).order_by('rate', '-created')[:50]
        context['bid_form'] = form_for_action(BidForm, 'create_bid', request)
        return context

    def action_create_bid(self, request, context, *args, **kwargs):
        form = context['bid_form']
        if form.is_valid():
            bid = form.save(commit=False)
            bid.market = context['market']
            bid.owner = context['avatar']
            bid.save()
            messages.info(request, 'Bid placed in market')
        else:
            messages.info(request, 'Oh, shi, please input correct values')
        return context

    def action_delete_bid(self, request, context, *args, **kwargs):
        bid = get_object_or_404(Bid, pk=request.POST.get('bid_pk', 0), owner=context['avatar'])
        bid.delete()
        messages.info(request, 'Bid succesfully deleted')


class VacancyListView(BaseGameView):
    template_name = 'vacancy/index.html'

    def get_context_data(self, request, **kwargs):
        context = super(VacancyListView, self).get_context_data(request, **kwargs)
        context['vacancy_list'] = Vacancy.objects.all().order_by('-created')
        return context

    def action_accept_vacancy(self, request, context, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=request.POST.get('vacancy_pk'))

        worker, _ = CompanyWorker.objects.get_or_create(
            company=vacancy.company, worker=context['avatar'],
            salary_per_hour=vacancy.salary_per_hour)
        worker.active = True
        worker.save()
        
        vacancy.delete()
        messages.info(request, 'You are hired!')

        return context


class CompanyView(BaseGameView):
    template_name = 'company/index.html'

    def get_context_data(self, request, **kwargs):
        context = super(CompanyView, self).get_context_data(request, **kwargs)
        context['company'] = Company.objects.get(pk=kwargs['company_pk'])
        context['create_vacancy_form'] = form_for_action(VacancyForm, 'create_vacancy', request)
        return context

    def action_create_vacancy(self, request, context, *args, **kwargs):
        form = context['create_vacancy_form']
        if form.is_valid():
            vacancy = form.save(commit=False)
            vacancy.company = context['company']
            vacancy.save()
        else:
            messages.info(request, 'Oh, shi, please input correct values')

    def action_delete_vacancy(self, request, context, *args, **kwargs):
        vacancy = get_object_or_404(Vacancy, pk=request.POST.get('vacancy_pk', 0), company__owner=context['avatar'])
        vacancy.delete()
        messages.info(request, 'Vacancy succesfully deleted')

    def action_work(self, request, context, *args, **kwargs):
        company_worker = get_object_or_404(CompanyWorker, active=True, company=context['company'], worker=context['avatar'])

        company_dublons = context['company'].owner.get_inventory_item(INVENTORY_TYPE.DUBLONS)
        avatar_dublons = context['avatar'].get_inventory_item(INVENTORY_TYPE.DUBLONS)

        context['avatar'].spent_hours(1)
        context['avatar'].adjust_health(-context['avatar'].health*0.02)
        if context['avatar'].health < 50:
            context['avatar'].adjust_happines(-10)
        elif context['avatar'].health < 90:
            context['avatar'].adjust_happines(10)
        context['avatar'].save()

        if company_dublons < company_worker.salary_per_hour:
            messages.info(request, 'Oh, shi, no money at company')
        else:
            avatar_dublons.quantity += company_worker.salary_per_hour
            company_dublons.quantity -= company_worker.salary_per_hour 

            avatar_dublons.save()
            company_dublons.save()

        return context
