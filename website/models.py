from django.db import models
from django.utils import timezone

# Create your models here.
class Gallery(models.Model):
    filename = models.CharField(max_length=200, default='', blank=True)
    image = models.ImageField(upload_to='Gallery/', default='', blank=True)
    created_at = models.DateTimeField(editable=True, default=timezone.now)

    def save(self, *args, **kwargs):
        if not self.filename:
            self.filename = str(self.image.name)
        super().save(*args, **kwargs)

    class Meta:
        db_table = "Gallery"

