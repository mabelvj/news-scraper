from django.db import models


class New(models.Model):
    title = models.CharField(max_length=200)
    entry_type = models.CharField(max_length=200)
    entry_text = models.TextField()
    url = models.CharField(max_length=200)
    date = models.DateField(blank=True, null=True)

    def __str__(self):
        return self.title
