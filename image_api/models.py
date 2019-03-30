from io import BytesIO
from typing import Tuple, Generator, Iterable
from uuid import (
    UUID,
    uuid4,
)
from xmlrpc.client import DateTime

from PIL import Image
from django.core.files import File
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
)
from django.db.models.fields.files import ImageFieldFile

IMAGE_FOLDER_NAME: str = 'gallery_images'
REDUCED_IMAGE_COMPRESSION_QUALITY = 85


class ReducedImageSize(object):

    # Target size of the largest image dimension
    THUMBNAIL_SIZE_PX: int = 300
    LARGE_SIZE_PX: int = 1000


def upload_to_uuid(instance: 'ImageFile', _filename: str):
    return f'{IMAGE_FOLDER_NAME}/{instance.pk}'


class ImageFile(Model):

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

    id: UUID = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    name: str = TextField()

    def __str__(self) -> str:
        return self.name


class GalleryItem(Model):

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
                    new_size
                )

                # Saving the file field also saves the related model
                field.file.save(None, resized_content)

    def __str__(self) -> str:
        return self.title


class ImageResizer(object):

    def __init__(self, image_file: File):

        self._image: Image = Image.open(image_file)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._image.close()

    def shrink_image_to_box_size(self, new_size: int) -> BytesIO:

        reduced_image = shrink_image_largest_dimension(
            self._image.copy(),  # We resize a copy of the original image
            new_size
        )

        output: BytesIO = BytesIO()
        reduced_image.save(
            output,
            format='JPEG',
            quality=REDUCED_IMAGE_COMPRESSION_QUALITY
        )

        return output


def shrink_image_largest_dimension(
    image: Image,
    target_size: int
) -> Image:
    """Preserves aspect ratio"""

    largest_dimension: int = max(image.height, image.width)

    if target_size >= largest_dimension:
        return image  # The image is small enough already

    scale_factor: float = target_size / largest_dimension

    # Compute the resized image dimensions
    if largest_dimension == image.height:

        # Set the height to the target size, compute the new width
        target_dimensions: Tuple[int, int] = (
            round(image.width * scale_factor),
            target_size
        )

    else:

        # Set the width to the target size, compute the new height
        target_dimensions: Tuple[int, int] = (
            target_size,
            round(image.height * scale_factor)
        )

    return image.resize(
        target_dimensions,
        Image.BICUBIC
    )
