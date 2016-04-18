import os

from django.conf import settings
from importlib import import_module

from django.core.exceptions import ImproperlyConfigured
from django.utils._os import safe_join

from cms_bs3_theme import conf
from django.forms import Form, ChoiceField, IntegerField, Select

themes = []
menus = []
for app in settings.INSTALLED_APPS:
    try:
        mod = import_module(app)
    except ImportError as e:
        raise ImproperlyConfigured('ImportError %s: %s' % (app, e.args[0]))

    cms_bs3_theme_templates = safe_join(os.path.abspath(os.path.join(
        os.path.dirname(mod.__file__),
        'templates',
        'cms_bs3_theme',
    )))

    if not os.path.isdir(cms_bs3_theme_templates):
        continue

    themes_dir = os.path.join(cms_bs3_theme_templates, 'themes')
    if os.path.isdir(themes_dir):
        themes += [(theme, theme) for theme in os.listdir(themes_dir)]

    menus_dir = os.path.join(cms_bs3_theme_templates, 'menus')
    if os.path.isdir(menus_dir):
        menus += list(map(lambda x: (os.path.join('cms_bs3_theme', 'menus', x), '.'.join(x.split('.')[:-1])),
                          os.listdir(menus_dir)))

class ChangeThemeOptionsForm(Form):
    bootstrap3_theme = ChoiceField(choices=sorted(themes))
    bootstrap3_menu_template = ChoiceField(choices=sorted(menus))
    bootstrap3_sidebar_cols = IntegerField(widget=Select(choices=[(i, i) for i in range(1, conf.BOOTSTRAP3_COLS)]))

    def __init__(self, *args, **kwargs):
        self.request = kwargs.pop('request')
        initial = self.request.session.get('cms_bs3_theme_conf', conf)
        initial = dict(map(lambda x: (str.lower(x[0]), x[1]), initial.items()))
        kwargs['initial'] = kwargs.get('initial') or initial
        super(ChangeThemeOptionsForm, self).__init__(*args, **kwargs)

    def save(self):
        self.request.session['cms_bs3_theme_conf'] = dict(map(lambda x: (str.upper(x[0]), x[1]),
                                                              self.cleaned_data.items()))
