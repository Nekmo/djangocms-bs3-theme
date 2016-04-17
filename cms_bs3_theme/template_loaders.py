# -*- coding: utf-8 -*-
from django.utils.safestring import SafeText

from . import conf
import django.template.loaders.app_directories

_cache = None
APP_NAME = 'cms_bs3_theme'



class AppDirectoriesLoader(django.template.loaders.app_directories.Loader):
    is_usable = conf.BOOTSTRAP3_THEME is not None

    def get_template_sources(self, template_name, template_dirs=None):
        if template_name.startswith(APP_NAME):
            root = APP_NAME + '/'
            template_name = SafeText(template_name.replace(root, '{}themes/{}/'.format(root, conf.BOOTSTRAP3_THEME)))
        return super(AppDirectoriesLoader, self).get_template_sources(
            template_name,
            # _get_bs3_app_template_dirs(template_dirs),
        )
