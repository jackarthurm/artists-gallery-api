from rest_framework.serializers import (
    HyperlinkedModelSerializer,
    ModelSerializer,
)
from rest_framework.fields import ImageField

from image_api.models import (
    GalleryItem,
    ItemTag,
    ImageFile,
)


class ItemTagSerializer(ModelSerializer):

    class Meta:
        model = ItemTag
        fields = (
            'name',
        )


class ImageFileSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = ImageFile
        fields = read_only_fields = (
            'id',
            'url',
            'height',
            'width',
        )

    url = ImageField(source='file')


class GalleryItemSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = GalleryItem
        fields = (
            'id',
            'url',
            'original_image',
            'large_image',
            'thumbnail_image',
            'title',
            'created_date',
            'description',
            'media_description',
            'size_description',
            'artist_name',
            'tags',
        )
        read_only_fields = (
            'id',
            'url',
            'tags',
            'large_image',
            'thumbnail_image',
        )

    original_image = ImageFileSerializer()
    large_image = ImageFileSerializer()
    thumbnail_image = ImageFileSerializer()

    tags = ItemTagSerializer(many=True)
