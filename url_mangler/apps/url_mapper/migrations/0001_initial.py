# Generated by Django 3.1.2 on 2020-11-01 04:58

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="UrlMapping",
            fields=[
                (
                    "id",
                    models.AutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "slug",
                    models.CharField(
                        help_text="Unique value for redirected URL",
                        max_length=2048,
                        unique=True,
                    ),
                ),
                ("destination_url", models.URLField(max_length=10000)),
                ("created_at", models.DateTimeField(auto_now_add=True, db_index=True)),
            ],
            options={
                "db_table": "url_mapping",
            },
        ),
    ]
