# Generated by Django 2.1.7 on 2019-03-31 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('image_api', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='imagefile',
            name='id',
            field=models.UUIDField(editable=False, primary_key=True, serialize=False, verbose_name='Object UUID'),
        ),
    ]