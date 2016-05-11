from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from jsonfield.fields import JSONField
from cms_bs3_theme import conf

CACHE_THEME = {}


class ThemeSiteManager(models.Manager):

    def get_by_site(self, site=None, request=None):
        assert site is not None or request is not None
        if conf.USE_THEME_SITE:
            site = site or get_current_site(request)
        return self.get(site=site)

    def get_theme_conf(self, site=None, request=None, fail=True):
        try:
            return self.get_by_site(site, request).theme.get_conf()
        except Exception as e:
            if fail:
                raise e
            else:
                return {}

    def get_theme_name(self, site=None, request=None, default=None):
        try:
            return self.get_theme_conf(site, request)['BOOTSTRAP3_THEME']
        except self.model.DoesNotExist as e:
            if default is None:
                raise e
            else:
                return default


class Theme(models.Model):
    name = models.CharField(max_length=40, db_index=True)
    conf = JSONField(default='{}')

    def get_conf(self):
        if self.pk in CACHE_THEME:
            return CACHE_THEME[self.pk]
        conf = self.conf
        CACHE_THEME[self.pk] = conf
        return conf


class ThemeSite(models.Model):
    site = models.ForeignKey(Site, unique=True)
    theme = models.ForeignKey(Theme)

    objects = ThemeSiteManager()