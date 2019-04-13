from rest_framework.serializers import ModelSerializer

from links_api.models import SocialMediaLinks


class SocialMediaLinksSerializer(ModelSerializer):

    class Meta:
        model = SocialMediaLinks
        fields = (
            'facebook',
            'instagram',
            'linkedin',
        )
