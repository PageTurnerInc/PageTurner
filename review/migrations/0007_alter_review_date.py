# Generated by Django 4.2.6 on 2023-10-28 11:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('review', '0006_alter_bookrating_rating'),
    ]

    operations = [
        migrations.AlterField(
            model_name='review',
            name='date',
            field=models.DateTimeField(),
        ),
    ]
