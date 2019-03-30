from django.contrib.admin import (
    ModelAdmin,
    site,
)
from django.core.files.uploadedfile import TemporaryUploadedFile
from django.forms import ModelForm
from django.forms.fields import ImageField


from image_api.models import (
    GalleryItem,
    ImageFile,
    ItemTag,
)


class GalleryItemForm(ModelForm):
    image_file = ImageField()

    class Meta:
        model = GalleryItem
        fields = (
            'image_file',
            'title',
            'artist_name',
            'created_date',
            'description',
            'media_description',
            'tags',
        )
        readonly_fields = (
            'id',
        )


class GalleryItemAdmin(ModelAdmin):
    form = GalleryItemForm

    def save_model(self, request, instance, form, _change):

        image_file: TemporaryUploadedFile = form.cleaned_data['image_file']
        category, _created = ImageFile.objects.get_or_create(file=image_file)
        instance.original_image = category

        super(GalleryItemAdmin, self).save_model(
            request,
            instance,
            form,
            _change
        )


site.register(ItemTag)
site.register(GalleryItem, GalleryItemAdmin)
