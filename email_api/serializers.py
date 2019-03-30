from rest_framework.serializers import HyperlinkedModelSerializer

from email_api.models import ContactEnquiry


class ContactEnquirySerializer(HyperlinkedModelSerializer):

    class Meta:
        model = ContactEnquiry
        fields = (
            'name',
            'email',
            'subject',
            'body',
        )
