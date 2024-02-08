# Generated by Django 5.0.1 on 2024-01-24 14:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [("wagtailcore", "0089_log_entry_data_json_null_to_object")]

    operations = [
        migrations.CreateModel(
            name="FlexPage",
            fields=[
                (
                    "page_ptr",
                    models.OneToOneField(
                        auto_created=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        parent_link=True,
                        primary_key=True,
                        serialize=False,
                        to="wagtailcore.page",
                    ),
                ),
                ("subtitle", models.CharField(blank=True, max_length=100, null=True)),
            ],
            options={"verbose_name": "Flex Page", "verbose_name_plural": "Flex Pages"},
            bases=("wagtailcore.page",),
        )
    ]
