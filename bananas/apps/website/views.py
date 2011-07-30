# -*- coding: utf-8; mode: django -*-
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from website.models import Avatar, ToManyHours, INVENTORY_TYPE


class AvatarView(TemplateResponseMixin, View):
    template_name = 'avatar/index.html'

    def get_context_data(self, request, **kwargs):
        return {
            'avatar': get_object_or_404(Avatar, owner=request.user, pk=kwargs['pk'])
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
        else:
            context['avatar'].adjust_health(-context['avatar'].health*0.01)
            messages.info(request, 'Tried to eat shoes, feels bad now')
        context['avatar'].save()            

        return context
