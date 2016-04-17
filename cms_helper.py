#!/usr/bin/env python
# -*- coding: utf-8 -*-
from __future__ import absolute_import, print_function, unicode_literals

from tempfile import mkdtemp


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
    ],
    LANGUAGE_CODE='en',
    LANGUAGES=(
        ('en', gettext('English')),
        ('es', gettext('Spanish')),
    ),
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
    PARLER_LANGUAGES={
        1: (
            {'code': 'en'},
            {'code': 'it'},
            {'code': 'fr'},
        ),
        2: (
            {'code': 'en'},
        ),
        'default': {
            'fallbacks': ['en'],
            'hide_untranslated': False,
        }
    },
    MIGRATION_MODULES={},
    CMS_TEMPLATES=(
        ('cms_bs3_theme/page.html', 'BS3 Page'),
        ('cms_bs3_theme/feature.html', 'BS3 Feature'),
    ),
)


def run():
    from djangocms_helper import runner
    runner.cms('cms_bs3_theme')

if __name__ == '__main__':
    run()
