# Generated by Django 4.2.6 on 2023-10-28 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("rak_buku", "0002_alter_rak_name"),
    ]

    operations = [
        migrations.AlterField(
            model_name="rak", name="name", field=models.CharField(max_length=16),
        ),
    ]
