from django.conf import settings

BOOTSTRAP3_COLS = 12
BOOTSTRAP3_SIDEBAR_COLS = 4
BOOTSTRAP3_THEME = 'default'
BOOTSTRAP3_MENU_TEMPLATE = 'cms_bs3_theme/menus/default.html'

# Override my settings usign Django Settings
for var_name, value in dict(locals()).items():
    if var_name.isupper():
        locals()[var_name] = getattr(settings, var_name, value)
