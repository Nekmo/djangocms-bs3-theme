#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals
import sys

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.append(os.path.join(BASE_DIR, 'demo'))

def gettext(s): return s

HELPER_SETTINGS = dict(
    # ROOT_URLCONF='tests.test_utils.urls',
    INSTALLED_APPS=[
        'djangocms_text_ckeditor',
        'djangocms_style',
        'djangocms_column',
        'djangocms_file',
        'djangocms_googlemap',
        'djangocms_inherit',
        'djangocms_link',
        'djangocms_picture',
        'djangocms_teaser',
        'djangocms_video',
        'bootstrap3',

        'cms_bs3_theme_solid',
        'demo_app',
    ],
    LANGUAGE_CODE='en',
    LANGUAGES=(
        ('en', gettext('English')),
        ('es', gettext('Spanish')),
    ),
    TEMPLATE_LOADERS=[
        # 'cms_bs3_theme.template_loaders.AppDirectoriesLoader',
    ],
    TEMPLATE_CONTEXT_PROCESSORS=[
        'cms_bs3_theme.context_processors.settings',
    ],
    CMS_LANGUAGES={
        1: [
            {
                'code': 'en',
                'name': gettext('English'),
                'public': True,
            },
            {
                'code': 'es',
                'name': gettext('Spanish'),
                'public': True,
            },
        ],
        2: [
            {
                'code': 'en',
                'name': gettext('English'),
                'public': True,
            },
        ],
        'default': {
            'hide_untranslated': False,
        },
    },
    CMS_TEMPLATES=(
        # ('cms_bs3_theme/page.html', 'BS3 Page'),
        ('cms_bs3_theme/fullwidth.html', 'BS3 Fullwidth'),
        ('cms_bs3_theme/sidebar_right.html', 'BS3 Sidebar Right'),
        ('cms_bs3_theme/sidebar_left.html', 'BS3 Sidebar Left'),
        ('cms_bs3_theme/feature.html', 'BS3 Feature'),
    ),
    BOOTSTRAP3_THEME='default',
    BOOTSTRAP3_MENU_TEMPLATE='cms_bs3_theme/menus/fluid-static-top.html',

    TEMPLATES=[
        {
            'BACKEND': 'django.template.backends.django.DjangoTemplates',
            'APP_DIRS': True,
            'OPTIONS': {
                # 'builtins': [
                #     'cms_bs3_theme.templatetags.bs3_tpl_loader'
                # ],
                'context_processors': [
                    'django.contrib.auth.context_processors.auth',
                    'django.contrib.messages.context_processors.messages',
                    'django.core.context_processors.i18n',
                    'django.core.context_processors.debug',
                    'django.core.context_processors.request',
                    'django.core.context_processors.media',
                    'django.core.context_processors.csrf',
                    'django.core.context_processors.tz',
                    'sekizai.context_processors.sekizai',
                    'django.core.context_processors.static',
                    'cms.context_processors.cms_settings',

                    'cms_bs3_theme.context_processors.settings',
                ],
            }
        },
    ]
)


def run():
    from djangocms_helper import runner
    runner.cms('cms_bs3_theme')

if __name__ == '__main__':
    run()
