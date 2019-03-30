from io import BytesIO
from typing import Tuple
from uuid import (
    UUID,
    uuid4,
)
from xmlrpc.client import DateTime


from django.db.models import (
    Model,
    ImageField,
    UUIDField,
    TextField,
    IntegerField,
    ManyToManyField,
    DateField,
    OneToOneField,
    CASCADE,
    Manager,
)
from django.db.models.fields.files import ImageFieldFile

from image_api.utils.image_resizer import ImageResizer

IMAGE_FOLDER_NAME: str = 'gallery_images'
REDUCED_IMAGE_COMPRESSION_QUALITY = 85


class ReducedImageSize(object):

    # Target size of the largest image dimension
    THUMBNAIL_SIZE_PX: int = 300
    LARGE_SIZE_PX: int = 1000


def upload_to_uuid(instance: 'ImageFile', _filename: str):
    return f'{IMAGE_FOLDER_NAME}/{instance.pk}'


class ImageFile(Model):

    objects: Manager = Manager()

    id: UUID = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    width: int = IntegerField(editable=False)
    height: int = IntegerField(editable=False)
    file: ImageFieldFile = ImageField(
        height_field='height',
        width_field='width',
        upload_to=upload_to_uuid
    )


class ItemTag(Model):

    class Meta:
        verbose_name: str = 'Gallery item tag'

    objects: Manager = Manager()

    id: UUID = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    name: str = TextField()

    def __str__(self) -> str:
        return self.name


class GalleryItem(Model):

    objects: Manager = Manager()

    id: UUID = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )

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
    created_date: DateTime = DateField(null=True, blank=True)
    description: str = TextField(blank=True)
    media_description: str = TextField(blank=True)
    artist_name: str = TextField()

    tags = ManyToManyField(to=ItemTag, blank=True)

    def save(self, *args, **kwargs) -> None:

        self._create_reduced_size_images()

        super(GalleryItem, self).save(*args, **kwargs)

    def _create_reduced_size_images(self) -> None:

        self.thumbnail_image = ImageFile()
        self.large_image = ImageFile()

        # Define the image file objects that need
        # resizing and their target sizes
        image_fields_to_resize: Tuple[Tuple[ImageFile, int]] = (
            (
                self.thumbnail_image,
                ReducedImageSize.THUMBNAIL_SIZE_PX
            ),
            (
                self.large_image,
                ReducedImageSize.LARGE_SIZE_PX
            ),
        )

        # The original image field is editable and
        # not nullable so we can assume it exists
        with ImageResizer(self.original_image.file.file) as resizer:

            for field, new_size in image_fields_to_resize:

                resized_content: BytesIO = resizer.shrink_image_to_box_size(
                    new_size,
                    REDUCED_IMAGE_COMPRESSION_QUALITY
                )

                # Saving the file field also saves the related model
                field.file.save(None, resized_content)

    def __str__(self) -> str:
        return self.title

