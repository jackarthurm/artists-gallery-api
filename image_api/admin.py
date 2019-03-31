from django.contrib.admin import (
    ModelAdmin,
    site,
)
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.db import transaction
from django.forms import ModelForm
from django.forms.fields import ImageField


from image_api.models import (
    GalleryItem,
    ImageFile,
    ItemTag,
)


GALLERY_ITEM_EDITABLE_FIELDS = (
    'image_file',
    'title',
    'artist_name',
    'created_date',
    'description',
    'media_description',
    'tags',
)


class GalleryItemAdminForm(ModelForm):
    image_file = ImageField()

    class Meta:
        model = GalleryItem
        fields = GALLERY_ITEM_EDITABLE_FIELDS


class GalleryItemAdmin(ModelAdmin):
    form = GalleryItemAdminForm

    filter_horizontal = (
        'tags',
    )

    def _original_image_id(self, obj: GalleryItem):
        return obj.original_image.id

    _original_image_id.short_description = 'Original image UUID'

    def _large_image_id(self, obj: GalleryItem):
        return obj.large_image.id

    _large_image_id.short_description = 'Large image UUID'

    def _thumbnail_image_id(self, obj: GalleryItem):
        return obj.thumbnail_image.id

    _thumbnail_image_id.short_description = 'Thumbnail image UUID'

    readonly_fields = (
        'id',
        '_original_image_id',
        '_large_image_id',
        '_thumbnail_image_id',
    )

    fieldsets = (
        (
            None,
            {
                'fields': GALLERY_ITEM_EDITABLE_FIELDS
            }
        ),
        (
            'Advanced information',
            {
                'classes': (
                    'collapse',
                ),
                'fields': readonly_fields
            }
        ),
    )

    def get_form(self, request, obj=None, **kwargs):

        form = super(GalleryItemAdmin, self).get_form(request, obj, **kwargs)

        # Pre-populate the image file field
        initial = obj.original_image.file if obj is not None else None

        form.base_fields['image_file'].initial = initial

        return form

    def save_model(
        self,
        request,
        instance: GalleryItem,
        form: GalleryItemAdminForm,
        change
    ):

        with transaction.atomic():

            image_file: TemporaryUploadedFile = form.cleaned_data['image_file']
            instance.set_image(image_file)

            super(GalleryItemAdmin, self).save_model(
                request,
                instance,
                form,
                change
            )


site.register(ItemTag)
site.register(GalleryItem, GalleryItemAdmin)
