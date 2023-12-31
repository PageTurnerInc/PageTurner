# Generated by Django 3.2.21 on 2023-10-28 21:06

import django.core.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0002_alter_bookrating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='bookrating',
            name='rating',
            field=models.FloatField(default=0.0, validators=[django.core.validators.MinValueValidator(1.0), django.core.validators.MaxValueValidator(5.0)]),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.IntegerField(validators=[django.core.validators.MinValueValidator(1), django.core.validators.MaxValueValidator(5)]),
        ),
    ]
