# Generated by Django 2.1.7 on 2019-03-31 23:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('email_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='contactenquiry',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False, verbose_name='Object UUID'),
        ),
    ]
