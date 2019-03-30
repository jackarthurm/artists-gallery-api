from rest_framework.serializers import HyperlinkedModelSerializer

from image_api.models import (
    GalleryItem,
    ItemTag,
    ImageFile,
)


class ItemTagSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = ItemTag
        fields = (
            'id',
            'name',
        )


class ImageFileSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = ImageFile
        fields = (
            'file',
            'height',
            'width',
        )


class GalleryItemSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = GalleryItem
        fields = (
            'id',
            'original_image',
            'large_image',
            'thumbnail_image',
            'title',
            'created_date',
            'description',
            'media_description',
            'artist_name',
            'tags',
        )

    original_image = ImageFileSerializer()
    large_image = ImageFileSerializer()
    thumbnail_image = ImageFileSerializer()
