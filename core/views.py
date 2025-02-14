from django.views.generic import TemplateView


class IndexView(TemplateView):
    template_name = 'core/index.html'


class IntegrationsView(TemplateView):
    template_name = 'core/integrations.html'
