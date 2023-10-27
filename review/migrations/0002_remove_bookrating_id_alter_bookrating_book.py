# Generated by Django 4.2.6 on 2023-10-26 13:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0002_auto_20231025_1931'),
        ('review', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='bookrating',
            name='id',
        ),
        migrations.AlterField(
            model_name='bookrating',
            name='book',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='book.book'),
        ),
    ]