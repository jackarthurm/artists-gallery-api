from django.contrib.admin import (
    site,
    ModelAdmin,
    StackedInline,
)

from image_api.models import (
    GalleryItem,
    ItemTag,
    ImageFile,
)


class GalleryItemInline(StackedInline):
    model = GalleryItem
    max_num = 1
    fk_name = 'original_image'


class ImageFileAdmin(ModelAdmin):
    inlines = (
        GalleryItemInline,
    )


site.register(ItemTag)
site.register(ImageFile, ImageFileAdmin)
