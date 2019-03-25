from rest_framework.serializers import HyperlinkedModelSerializer

from image_api.models import (
    GalleryItem,
    ItemTag,
)


class ItemTagSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = ItemTag
        fields = (
            'id',
            'name',
        )


class GalleryItemSerializer(HyperlinkedModelSerializer):

    class Meta:
        model = GalleryItem
        fields = (
            'id',
            'original_width',
            'original_height',
            'reduced_width',
            'reduced_height',
            'title',
            'description',
            'media_description',
            'artist_name',
            'tags',
        )
