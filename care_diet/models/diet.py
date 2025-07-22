from django.db import models
import uuid

class Diet(models.Model):
    external_id = models.UUIDField(default=uuid.uuid4, editable=False, unique=True)
    name = models.CharField(max_length=255)
    created_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
