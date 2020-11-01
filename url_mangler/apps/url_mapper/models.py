from django.db import models


class UrlMapping(models.Model):
    slug = models.CharField(
        max_length=2048,
        unique=True,  # implies index creation
        help_text="Unique value for redirected URL",
    )
    destination_url = models.URLField(max_length=10000)
    created_at = models.DateTimeField(auto_now_add=True, db_index=True)

    class Meta:
        db_table = "url_mapping"
