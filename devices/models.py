from django.db import models
from core.models import BaseModel
from accounts.models import User


class Device(BaseModel):
    owner = models.ForeignKey(User, related_name="devices")
    ip = models.GenericIPAddressField()
    status = models.BooleanField(default=False)
    connected = models.BooleanField(default=False)
