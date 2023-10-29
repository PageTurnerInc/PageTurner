from django.db import migrations, models
import django.db.models.deletion
import isbn_field.fields
import isbn_field.validators


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Book',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('isbn', isbn_field.fields.ISBNField(max_length=28, validators=[isbn_field.validators.ISBNValidator], verbose_name='ISBN')),
                ('book_title', models.TextField(blank=True, null=True)),
                ('book_author', models.TextField(blank=True, null=True)),
                ('year_of_publication', models.IntegerField(blank=True, null=True)),
                ('publisher', models.TextField(blank=True, null=True)),
                ('image_url_s', models.TextField(blank=True, null=True)),
                ('image_url_m', models.TextField(blank=True, null=True)),
                ('image_url_l', models.TextField(blank=True, null=True)),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='main.account')),
            ],
        ),
    ]
