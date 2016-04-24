from django.core.urlresolvers import reverse
from django.views.generic import FormView
from .forms import ChangeThemeOptionsForm


class ChangeThemeOptionsView(FormView):
    template_name = 'demo_app/change_theme.html'
    form_class = ChangeThemeOptionsForm

    def get_form_kwargs(self):
        kwargs = super(ChangeThemeOptionsView, self).get_form_kwargs()
        kwargs['request'] = self.request
        return kwargs

    def form_valid(self, form):
        form.save()
        return super(ChangeThemeOptionsView, self).form_valid(form)

    def get_success_url(self):
        return reverse('change_theme_options')
