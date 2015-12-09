from django.db import models
from core.models import BaseModel
from accounts.models import User

class DeviceModel(BaseModel):
    ip = models.GenericIPAddressField()
    device_id = models.CharField(max_length=16)
    status = models.BooleanField(default=False)
    connected = models.BooleanField(default=False)

    def check_validation_code(self, code):
        return DeviceValidation.objects.filter(
            device_id=self.device_id,
            code=self.code).exists()

    class Meta:
        abstract = True


class Device(DeviceModel):
    owner = models.ForeignKey(User, related_name="devices")

class DeviceTemp(DeviceModel):
    processed = models.BooleanField(default=False)

    def generate_device(self):
        return Device(
            ip = ip,
            device_id = device_id,
            status = status,
            connected = connected
        )

class DeviceValidation(BaseModel):
    device_id = models.CharField(max_length=16)
    code = models.CharField(max_length=16)
