from PIL import Image
from io import FileIO
from typing import Tuple


class ImageResizer(object):

    def __init__(self, image_file: FileIO):

        self._image: Image = Image.open(image_file)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self._image.close()

    def shrink_image_to_box_size(
        self,
        new_size: int,
        fout: FileIO,
        compression_quality: int = 85,
        save_format: str = 'JPEG'
    ) -> None:

        resized_image: Image = shrink_image_largest_dimension(
            self._image.copy(),  # We resize a copy of the original image
            new_size
        )

        resized_image.save(
            fout,
            format=save_format,
            quality=compression_quality
        )


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
