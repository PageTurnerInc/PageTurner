# Generated by Django 3.2.9 on 2023-10-22 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('wishlist', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='book',
            name='cover_image',
            field=models.ImageField(default=2, upload_to='book_covers/'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='price',
            field=models.DecimalField(decimal_places=2, default=2, max_digits=6),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='book',
            name='synopsis',
            field=models.TextField(default=2),
            preserve_default=False,
        ),
    ]
