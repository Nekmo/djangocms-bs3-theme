from django.contrib import admin

from cms_bs3_theme.models import ThemeSite, Theme


class ThemeAdmin(admin.ModelAdmin):
    pass

admin.site.register(Theme, ThemeAdmin)


class ThemeSiteAdmin(admin.ModelAdmin):
    pass

admin.site.register(ThemeSite, ThemeSiteAdmin)
