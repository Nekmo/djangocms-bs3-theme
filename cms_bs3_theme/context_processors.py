# -*- coding: utf-8 -*-


def settings(request):
    """
    """
    from . import conf
    conf = dict(vars(conf))
    data = request.session.get('cms_bs3_theme_conf', {})
    conf.update(data)
    return {'bs3_conf': conf}
