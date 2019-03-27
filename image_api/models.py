from io import BytesIO
from uuid import (
    UUID,
    uuid4,
)
from PIL import Image
from django.core.files import File
from django.core.files.uploadedfile import (
    InMemoryUploadedFile,
    SimpleUploadedFile,
)

from django.db.models import (
    Model,
    ImageField,
    UUIDField,
    TextField,
    IntegerField,
    ManyToManyField,
)


REDUCED_IMAGE_WIDTH: int = 500
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

    def save(self, *args, **kwargs):

        self.reduced_image = self._create_reduced_image()
        self.reduced_image.file.content_type = (
            self.original_image.file.content_type
        )

        super(GalleryItem, self).save(*args, **kwargs)

    def _create_reduced_image(
        self,
        reduced_width: int = REDUCED_IMAGE_WIDTH,
        compression_quality: int = REDUCED_IMAGE_COMPRESSION_QUALITY
    ) -> File:

        # Resize the original sized image
        image: Image = Image.open(self.original_image.file)
        reduced_image: Image = image.copy()
        image.close()

        # Compute the resized image dimensions
        fractional_width: float = reduced_width / reduced_image.size[0]

        reduced_height: int = round(
            reduced_image.size[1] * fractional_width
        )

        reduced_image = reduced_image.resize(
            (reduced_width, reduced_height),
            Image.BICUBIC
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

    def __str__(self):
        return self.title
