from io import BytesIO
from typing import Tuple

from django.core.files import File
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


class ReducedImageSize(object):

    # Target size of the largest image dimension
    THUMBNAIL_SIZE_PX: int = 300
    LARGE_SIZE_PX: int = 1000


def upload_to_uuid(instance: 'ImageFile', _filename: str):
    return f'{IMAGE_FOLDER_NAME}/{instance.pk}'


class ImageFile(UUIDModel):

    objects: Manager = Manager()

    width: int = IntegerField(editable=False)
    height: int = IntegerField(editable=False)
    file: ImageFieldFile = ImageField(
        height_field='height',
        width_field='width',
        upload_to=upload_to_uuid,
        blank=False
    )


class ItemTag(Model):

    class Meta:
        verbose_name: str = 'gallery item tag'

    objects: Manager = Manager()

    name: str = CharField(primary_key=True, max_length=32)

    def __str__(self) -> str:
        return f'Gallery item tag "{self.name}"'


class GalleryItem(UUIDModel):

    class Meta:
        verbose_name = 'gallery item'

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

            self._create_reduced_size_images()

            super(GalleryItem, self).save(*args, **kwargs)

    def set_image(self, image_file: File) -> None:

        try:
            img: ImageFile = self.original_image
        except ImageFile.DoesNotExist:
            img: ImageFile = ImageFile()

        img.file = image_file
        img.save()

        self.original_image = img

    def _create_reduced_size_images(self) -> None:

        try:
            thumbnail_image: ImageFile = self.thumbnail_image
        except ImageFile.DoesNotExist:
            thumbnail_image: ImageFile = ImageFile()

        try:
            large_image: ImageFile = self.large_image
        except ImageFile.DoesNotExist:
            large_image: ImageFile = ImageFile()

        # Define the image file objects that need
        # resizing and their target sizes
        images_to_resize: Tuple[Tuple[ImageFile, int]] = (
            (
                thumbnail_image,
                ReducedImageSize.THUMBNAIL_SIZE_PX
            ),
            (
                large_image,
                ReducedImageSize.LARGE_SIZE_PX
            ),
        )

        # The original image field is editable and
        # not nullable so we can assume it exists
        with ImageResizer(self.original_image.file.file) as resizer:

            for img, new_size in images_to_resize:

                resized_content: BytesIO = resizer.shrink_image_to_box_size(
                    new_size,
                    REDUCED_IMAGE_COMPRESSION_QUALITY
                )

                # Saving the file field also creates the model
                img.file.save(None, resized_content)

        # Now the relations are saved we can set them as model attributes
        self.thumbnail_image = thumbnail_image
        self.large_image = large_image

    def __str__(self) -> str:
        return f'Gallery item for "{self.title}"'
