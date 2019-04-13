from django.http import Http404
from rest_framework.mixins import ListModelMixin
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from links_api.models import SocialMediaLinks
from links_api.serializers import SocialMediaLinksSerializer


class SocialMediaLinksViewSet(ListModelMixin, GenericViewSet):

    queryset = SocialMediaLinks.objects.all()
    serializer_class = SocialMediaLinksSerializer

    def get_object(self):

        try:
            return SocialMediaLinks.objects.get()
        except SocialMediaLinks.DoesNotExist:
            raise Http404

    def list(self, request, *args, **kwargs):

        serializer = self.get_serializer(
            instance=self.get_object()
        )
        return Response(serializer.data)
