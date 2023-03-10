# Generated by Django 4.1.4 on 2023-02-24 08:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("offers", "0002_category_offer_delete_offers_category_offer_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="category",
            name="offer",
        ),
        migrations.RemoveField(
            model_name="category",
            name="request",
        ),
        migrations.AddField(
            model_name="offer",
            name="category",
            field=models.ForeignKey(
                default=False,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="category",
                to="offers.category",
            ),
        ),
    ]
