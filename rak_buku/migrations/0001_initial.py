from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('book', '0001_initial'),
        ('main', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Rak',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=16)),
                ('description', models.TextField()),
                ('books', models.ManyToManyField(to='book.book')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main.account')),
            ],
        ),
    ]
