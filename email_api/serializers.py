from rest_framework.serializers import ModelSerializer

from email_api.models import ContactEnquiry


class ContactEnquirySerializer(ModelSerializer):

    class Meta:
        model = ContactEnquiry
        fields = (
            'name',
            'email',
            'subject',
            'body',
        )
