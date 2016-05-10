from django.contrib.sites.models import Site
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


class Theme(models.Model):
    name = models.CharField(max_length=40, db_index=True)
    conf = JSONField(default='{}')

    objects = ThemeManager()

    def get_conf(self):
        conf = self.conf
        CACHE_THEME[self.pk] = conf
        return conf


class ThemeSite(models.Model):
    site = models.ForeignKey(Site, unique=True)
    theme = models.ForeignKey(Theme)
