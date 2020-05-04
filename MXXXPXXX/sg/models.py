from django.db import models


# Create your models here.
class Keyword(models.Model):
    keyword_text = models.CharField(max_length=200)

    def __str__(self):
        return self.keyword_text
