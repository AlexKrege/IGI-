from django.db import models

class Promocode(models.Model):
    code = models.CharField(max_length=50, unique=True)
    discount_percent = models.IntegerField()
    valid_from = models.DateField()
    valid_to = models.DateField()
    is_active = models.BooleanField(default=True)
    archived = models.BooleanField(default=False)

    def __str__(self):
        return self.code