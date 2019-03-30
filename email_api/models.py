from uuid import (
    UUID,
    uuid4,
)

from django.db.models import (
    Model,
    EmailField,
    BooleanField,
    UUIDField,
    Manager,
    CharField,
)


class ContactEnquiry(Model):

    class Meta:
        verbose_name = 'Contact enquiry'
        verbose_name_plural = 'Contact enquiries'

    objects = Manager()

    id: UUID = UUIDField(
        primary_key=True,
        default=uuid4,
        editable=False
    )
    name = CharField(blank=True, max_length=70)
    email = EmailField(blank=True, max_length=254)
    subject = CharField(blank=True, max_length=78)
    body = CharField(blank=True, max_length=10000)
    email_sent_successfully = BooleanField(editable=False)

    def save(self, *args, **kwargs) -> None:

        # TODO: Attempt to send email here
        self.email_sent_successfully = False

        super(ContactEnquiry, self).save(*args, **kwargs)
