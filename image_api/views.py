from rest_framework.viewsets import ReadOnlyModelViewSet

from image_api.models import (
    GalleryItem,
    ItemTag,
)
from image_api.serializers import (
    GalleryItemSerializer,
    ItemTagSerializer,
)


class ItemTagViewSet(ReadOnlyModelViewSet):

    queryset = ItemTag.objects.all()
    serializer_class = ItemTagSerializer


class GalleryViewSet(ReadOnlyModelViewSet):

    class Meta:
        fields = (
            'name',
        )

    queryset = GalleryItem.objects.all()
    serializer_class = GalleryItemSerializer
