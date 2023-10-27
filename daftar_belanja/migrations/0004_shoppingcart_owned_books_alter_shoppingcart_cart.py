# Generated by Django 4.2.4 on 2023-10-27 10:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('book', '0003_book_user'),
        ('daftar_belanja', '0003_alter_shoppingcart_cart_delete_orderedbook'),
    ]

    operations = [
        migrations.AddField(
            model_name='shoppingcart',
            name='owned_books',
            field=models.ManyToManyField(related_name='owned_books', to='book.book'),
        ),
        migrations.AlterField(
            model_name='shoppingcart',
            name='cart',
            field=models.ManyToManyField(related_name='cart', to='book.book'),
        ),
    ]
