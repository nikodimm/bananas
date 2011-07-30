# -*- coding: utf-8; mode: django -*-
from django.contrib import messages
from django.shortcuts import get_object_or_404
from django.views.generic.base import TemplateResponseMixin, View
from website.models import Avatar, ToManyHoursException

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
            context = handler(context, *args, **kwargs)
        except ToManyHoursException:
            messages.info(request, 'No more hours today, take a rest')

        return self.render_to_response(context)

    def action_sleep(self, context, *args, **kwargs):
        """
        Sleep action, resotres heals poinst and make
        feels happy
        """
        context['avatar'].spent_hours(8)
        context['avatar'].health = max(context['avatar'].health*0.1, 100)
        context['avatar'].save()
        return context
