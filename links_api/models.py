from django.core.exceptions import ObjectDoesNotExist
from django.db.models import (
    URLField,
    Manager,
)

from solo.models import SingletonModel


class SocialMediaLinks(SingletonModel):

    class Meta:
        verbose_name = 'social media links'

    objects: Manager
    DoesNotExist: ObjectDoesNotExist

    facebook = URLField(null=True, blank=True)
    instagram = URLField(null=True, blank=True)
    linkedin = URLField(null=True, blank=True)

    def __str__(self):
        return 'Social media links configuration'
