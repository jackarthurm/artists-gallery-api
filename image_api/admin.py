from django.contrib.admin import site

from image_api.models import (
    GalleryItem,
    ItemTag,
)


site.register(GalleryItem)
site.register(ItemTag)
