# -*- coding: utf-8 -*-
# from cms_bs3_theme.models import ThemeSite


def settings(request):
    """
    """
    from . import conf
    conf = dict(vars(conf))
    # conf.update(ThemeSite.objects.get_theme_conf(request=request, fail=False))
    data = request.session.get('cms_bs3_theme_conf', {})
    conf.update(data)
    return {'bs3_conf': conf}
