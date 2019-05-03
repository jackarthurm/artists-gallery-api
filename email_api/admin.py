from django.contrib.admin import (
    site,
    ModelAdmin,
)

from email_api.models import (
    ContactEnquiry,
    ContactRecipient,
)


class ContactEnquiryAdmin(ModelAdmin):

    def has_change_permission(self, *args, **kwargs):
        return False  # Enquiry objects are read-only

    def has_add_permission(self, *args, **kwargs):
        return False  # Enquiry objects shouldn't be created directly

    def email_sent_ok(self, obj: ContactEnquiry):
        return '✓' if obj.email_sent_ok else '✗'

    email_sent_ok.short_description = 'Email sent successfully?'

    readonly_fields = (
        'name',
        'email',
        'subject',
        'body',
        'created_time',
        'email_sent_ok',
        'id',
        'email_error',
    )

    fieldsets = (
        (
            None,
            {
                'fields': (
                    'name',
                    'email',
                    'subject',
                    'body',
                    'created_time',
                    'email_sent_ok',
                )
            }
        ),
        (
            'Advanced information',
            {
                'classes': (
                    'collapse',
                ),
                'fields': (
                    'id',
                    'email_error'
                ),
            }
        ),
    )


site.register(ContactEnquiry, ContactEnquiryAdmin)
site.register(ContactRecipient)
