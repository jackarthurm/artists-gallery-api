from smtplib import (
    SMTPException,
    SMTPResponseException,
)
from typing import (
    Optional,
    List,
)

from django.db.models import (
    EmailField,
    Manager,
    CharField,
    TextField,
    DateTimeField,
    Model,
    BooleanField,
)

from gallery_shared.models import UUIDModel


class ContactEnquiry(UUIDModel):

    objects: Manager

    class Meta:
        verbose_name = 'contact enquiry'
        verbose_name_plural = 'contact enquiries'

    name: str = CharField(
        max_length=70,
        verbose_name='Contact name'
    )
    email: str = EmailField(
        max_length=254,
        verbose_name='Contact email address'
    )
    subject: str = CharField(
        blank=True,
        max_length=78,
        verbose_name='Subject of enquiry'
    )
    body: str = CharField(
        blank=True,
        max_length=2000,
        verbose_name='Message text'
    )
    email_error: str = TextField(
        null=True,
        editable=False,
        verbose_name='Email error message'
    )

    created_time = DateTimeField(auto_now_add=True)

    @property
    def email_sent_ok(self) -> Optional[bool]:

        return self.pk and self.email_error is None

    def set_email_error(self, e: SMTPException):

        if isinstance(e, SMTPResponseException):

            smtp_err: str = e.smtp_error.decode('utf-8')

            err_text: str = (
                f'SMTP response error with status code {e.smtp_code} - '
                f'"{smtp_err}"'
            )

        else:
            err_text: str = f'SMTP error - "{e}"'

        self.email_error = err_text

    def __str__(self) -> str:

        return self.subject


class ContactRecipientManager(Manager):

    def emails(self) -> List[str]:

        return list(
            self.all().filter(send_email=True).values_list(
                'email',
                flat=True
            )
        )


class ContactRecipient(Model):

    class Meta:
        verbose_name = 'contact recipient'

    objects = ContactRecipientManager()

    email = EmailField()
    name = CharField(null=True, blank=True, max_length=78)
    send_email = BooleanField(
        default=True,
        help_text='Whether or not to send emails to this contact recipient'
    )

    def __str__(self):
        return self.name or self.email
