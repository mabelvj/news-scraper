from django.db import models


class News(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()
    entry_type = models.CharField(max_length=200)
    entry_text = models.TextField()
    url = models.CharField(max_length=200)
    published_date = models.DateTimeField(
        blank=True, null=True)

    def __str__(self):
        return self.title
