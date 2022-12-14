# Generated by Django 4.1.3 on 2022-12-11 23:02

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0008_rename_customer_order_user_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cart',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date_ordered', models.DateTimeField(auto_now=True)),
                ('quantity', models.IntegerField(blank=True, default=0, null=True)),
                ('item', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='cart', to='shop.item')),
                ('user', models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, related_name='shopping_cart', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='item',
        ),
        migrations.RemoveField(
            model_name='orderitem',
            name='order',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
        migrations.DeleteModel(
            name='OrderItem',
        ),
    ]
