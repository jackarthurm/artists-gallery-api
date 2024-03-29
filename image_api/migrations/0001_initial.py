# Generated by Django 2.1.7 on 2019-03-31 11:19

from django.db import migrations, models
import django.db.models.deletion
import image_api.models
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GalleryItem',
            fields=[
                ('id', models.UUIDField(editable=False, primary_key=True, serialize=False, verbose_name='Object UUID')),
                ('title', models.TextField()),
                ('created_date', models.DateField(blank=True, null=True)),
                ('description', models.TextField(blank=True)),
                ('media_description', models.TextField(blank=True)),
                ('artist_name', models.TextField()),
            ],
            options={
                'verbose_name': 'gallery item',
            },
        ),
        migrations.CreateModel(
            name='ImageFile',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False, verbose_name='Object UUID')),
                ('width', models.IntegerField(editable=False)),
                ('height', models.IntegerField(editable=False)),
                ('file', models.ImageField(height_field='height', upload_to=image_api.models.upload_to_uuid, width_field='width')),
            ],
        ),
        migrations.CreateModel(
            name='ItemTag',
            fields=[
                ('name', models.CharField(max_length=32, primary_key=True, serialize=False)),
            ],
            options={
                'verbose_name': 'gallery item tag',
            },
        ),
        migrations.AddField(
            model_name='galleryitem',
            name='large_image',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='gallery_item_as_large_image', to='image_api.ImageFile'),
        ),
        migrations.AddField(
            model_name='galleryitem',
            name='original_image',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='gallery_item_as_original_image', to='image_api.ImageFile'),
        ),
        migrations.AddField(
            model_name='galleryitem',
            name='tags',
            field=models.ManyToManyField(blank=True, to='image_api.ItemTag'),
        ),
        migrations.AddField(
            model_name='galleryitem',
            name='thumbnail_image',
            field=models.OneToOneField(editable=False, on_delete=django.db.models.deletion.CASCADE, related_name='gallery_item_as_thumbnail_image', to='image_api.ImageFile'),
        ),
    ]
