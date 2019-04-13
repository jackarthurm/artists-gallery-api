from django.contrib.admin import site

from solo.admin import SingletonModelAdmin

from links_api.models import SocialMediaLinks


class PatchedSingletonModelAdmin(SingletonModelAdmin):
    """The django-solo model admin, patched with the changes from
    https://github.com/lazybird/django-solo/pull/66
    """

    object_history_template = 'object_history.html'
    change_form_template = 'change_form.html'


site.register(SocialMediaLinks, PatchedSingletonModelAdmin)
