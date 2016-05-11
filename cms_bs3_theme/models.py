from django.contrib.sites.models import Site
from django.contrib.sites.shortcuts import get_current_site
from django.db import models
from django.utils import six
from jsonfield.fields import JSONField


CACHE_THEME = {}


class ThemeManager(models.Manager):

    def get_theme_conf(self, name_or_pk):
        if name_or_pk in CACHE_THEME:
            return CACHE_THEME[name_or_pk]
        query = {'name': name_or_pk} if isinstance(name_or_pk, six.string_types) else {'pk': name_or_pk}
        return self.model.objects.get(*query).get_conf()

    def get_theme_name(self, name_or_pk, default=None):
        try:
            return self.get_theme_conf(name_or_pk)['BOOTSTRAP3_THEME']
        except self.model.DoesNotExist as e:
            if default is None:
                raise e
            else:
                return default


class ThemeSiteManager(models.Manager):

    def get_by_site(self, site=None, request=None):
        assert site is not None or request is not None
        site = site or get_current_site(request)
        return self.get(site=site)

    def get_theme_conf(self, site=None, request=None):
        return self.get_by_site(site, request).theme.get_conf()

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

    objects = ThemeManager()

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