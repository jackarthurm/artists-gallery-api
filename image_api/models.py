from uuid import (
    UUID,
    uuid4,
)

from django.core.files import File
from django.core.files.uploadedfile import SimpleUploadedFile
from django.db import transaction
from django.db.models import (
    Model,
    ImageField,
    TextField,
    IntegerField,
    ManyToManyField,
    DateField,
    OneToOneField,
    CASCADE,
    Manager,
    CharField,
)
from django.db.models.fields.files import ImageFieldFile

from gallery_shared.models import UUIDModel
from image_api.utils.image_resizer import ImageResizer


IMAGE_FOLDER_NAME: str = 'gallery_images'
REDUCED_IMAGE_COMPRESSION_QUALITY = 85


class ReducedImageSizePx(object):

    # Target size of the largest image dimension
    THUMBNAIL: int = 300
    LARGE: int = 1000


def upload_to_uuid(instance: 'ImageFile', _filename: str):

    if not isinstance(instance.pk, UUID):
        raise ValueError('Instance ID must be set')

    return f'{IMAGE_FOLDER_NAME}/{instance.pk}'


class ImageFile(UUIDModel):

    objects: Manager = Manager()

    width: int = IntegerField(editable=False)
    height: int = IntegerField(editable=False)
    file: ImageFieldFile = ImageField(
        height_field='height',
        width_field='width',
        upload_to=upload_to_uuid
    )


class ItemTag(Model):

    class Meta:
        verbose_name: str = 'gallery item tag'
        ordering = (
            'name',
        )

    objects: Manager = Manager()

    name: str = CharField(primary_key=True, max_length=32)

    def __str__(self) -> str:
        return self.name


class GalleryItem(UUIDModel):

    class Meta:
        verbose_name = 'gallery item'
        ordering = (
            '-created_date',
            'title',
        )

    objects: Manager = Manager()

    original_image: ImageFile = OneToOneField(
        to=ImageFile,
        on_delete=CASCADE,
        related_name='gallery_item_as_original_image'
    )

    large_image: ImageFile = OneToOneField(
        to=ImageFile,
        on_delete=CASCADE,
        editable=False,
        related_name='gallery_item_as_large_image'
    )

    thumbnail_image: ImageFile = OneToOneField(
        to=ImageFile,
        on_delete=CASCADE,
        editable=False,
        related_name='gallery_item_as_thumbnail_image'
    )

    title: str = TextField()
    created_date = DateField(null=True, blank=True)
    description: str = TextField(blank=True)
    media_description: str = TextField(blank=True)
    artist_name: str = TextField()

    tags = ManyToManyField(to=ItemTag, blank=True)

    def save(self, *args, **kwargs) -> None:

        with transaction.atomic():

            self._save_reduced_size_images()

            super(GalleryItem, self).save(*args, **kwargs)

    def save_image(self, file: File) -> None:

        self._save_image_field('original_image', file)

    def _save_image_field(self, image_field: str, file: File) -> None:

        try:
            img: ImageFile = getattr(self, image_field)
        except ImageFile.DoesNotExist:
            img: ImageFile = ImageFile(id=uuid4())

        # Saving the file field saves the related model too
        img.file.save(
            None,
            file
        )

        setattr(self, image_field, img)

    def _save_reduced_size_images(self) -> None:

        # The original image field is editable and
        # not nullable so we can assume it exists
        with ImageResizer(self.original_image.file.file) as resizer:

            file = SimpleUploadedFile(None, None, 'image/jpeg')

            resizer.shrink_image_to_box_size(
                new_size=ReducedImageSizePx.THUMBNAIL,
                fout=file.file,
                compression_quality=REDUCED_IMAGE_COMPRESSION_QUALITY,
                save_format='JPEG',
            )

            self._save_image_field('thumbnail_image', file)

            file = SimpleUploadedFile(None, None, 'image/jpeg')

            resizer.shrink_image_to_box_size(
                new_size=ReducedImageSizePx.LARGE,
                fout=file.file,
                compression_quality=REDUCED_IMAGE_COMPRESSION_QUALITY,
                save_format='JPEG',
            )

            self._save_image_field('large_image', file)

    def __str__(self) -> str:
        return f'Gallery item for "{self.title}"'
