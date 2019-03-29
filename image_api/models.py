from io import BytesIO
from typing import Tuple
from uuid import (
    UUID,
    uuid4,
)
from PIL import Image
from django.core.files import File
from django.db.models import (
    Model,
    ImageField,
    UUIDField,
    TextField,
    IntegerField,
    ManyToManyField,
)


REDUCED_IMAGE_SIZE_PX: int = 300  # Target size of the largest image dimension
REDUCED_IMAGE_COMPRESSION_QUALITY = 85


def upload_to_original_size_folder(instance: 'GalleryItem', _filename: str):
    return f'original_size_gallery_items/{instance.pk}'


def upload_to_reduced_size_folder(instance: 'GalleryItem', _filename: str):
    return f'reduced_size_gallery_items/{instance.pk}'


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

    original_width: int = IntegerField(editable=False)
    original_height: int = IntegerField(editable=False)
    original_image = ImageField(
        height_field='original_height',
        width_field='original_width',
        upload_to=upload_to_original_size_folder
    )

    reduced_width: int = IntegerField(editable=False)
    reduced_height: int = IntegerField(editable=False)
    reduced_image = ImageField(
        height_field='reduced_height',
        width_field='reduced_width',
        upload_to=upload_to_reduced_size_folder,
        editable=False
    )

    title: str = TextField()
    description: str = TextField(blank=True)
    media_description: str = TextField(blank=True)
    artist_name: str = TextField()

    tags = ManyToManyField(to=ItemTag, blank=True)

    def save(self, *args, **kwargs) -> None:

        self.reduced_image = self._create_reduced_image()
        self.reduced_image.file.content_type = (
            self.original_image.file.content_type
        )

        super(GalleryItem, self).save(*args, **kwargs)

    def _create_reduced_image(
        self,
        reduced_size: int = REDUCED_IMAGE_SIZE_PX,
        compression_quality: int = REDUCED_IMAGE_COMPRESSION_QUALITY
    ) -> File:

        # Resize a copy of the original image
        image: Image = Image.open(self.original_image.file)
        reduced_image: Image = image.copy()
        image.close()

        reduced_image = shrink_image_to_largest_dimension(
            reduced_image,
            reduced_size
        )

        output: BytesIO = BytesIO()
        reduced_image.save(
            output,
            format='JPEG',
            quality=compression_quality
        )

        return File(
            output,
            self.original_image.name
        )

    def __str__(self) -> str:
        return self.title


def shrink_image_to_largest_dimension(
    image: Image,
    target_size: int
) -> Image:
    """Preserving aspect ratio"""

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
