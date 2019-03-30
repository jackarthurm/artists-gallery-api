# Generated by Django 2.1.7 on 2019-03-30 14:46

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='ContactEnquiry',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('name', models.CharField(blank=True, max_length=70)),
                ('email', models.EmailField(blank=True, max_length=254)),
                ('subject', models.CharField(blank=True, max_length=78)),
                ('body', models.CharField(blank=True, max_length=10000)),
                ('email_sent_successfully', models.BooleanField(editable=False)),
            ],
        ),
    ]
