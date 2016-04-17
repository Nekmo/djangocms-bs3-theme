from cms.app_base import CMSApp
from cms.apphook_pool import apphook_pool
from django.utils.translation import ugettext_lazy as _

class BS3DemoApphook(CMSApp):
    name = _("DjangoCMS BS3 Theme Demo")
    urls = ['demo_app.urls']

apphook_pool.register(BS3DemoApphook)
