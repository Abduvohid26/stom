import uuid

from django.core.validators import RegexValidator
from django.db import models
from django.contrib.auth.models import AbstractUser
from rest_framework_simplejwt.tokens import RefreshToken

NAQD, KARTA = ("naqd", "karta")
phone_regex = RegexValidator(
    regex=r'^\+998([- ])?(90|91|93|94|95|98|99|33|97|71|88|)([- ])?(\d{3})([- ])?(\d{2})([- ])?(\d{2})$',
    message='Invalid phone number'
)

class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    username = models.CharField(unique=True, max_length=250)
    password = models.CharField(max_length=250)
    confirm_password = models.CharField(max_length=250)

    def __str__(self):
        return self.username

    def token(self):
        refresh = RefreshToken.for_user(self)
        return {
            'access_token': str(refresh.access_token),
            'refresh_token': str(refresh)
        }

    def save(self, *args, **kwargs):
        super(User, self).save(*args, **kwargs)


class Patients(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    first_name = models.CharField(max_length=250, null=True, blank=True)
    last_name = models.CharField(max_length=250, null=True, blank=True)
    age = models.IntegerField(null=True, blank=True)
    address = models.CharField(max_length=250, null=True, blank=True)
    phone = models.CharField(max_length=250, null=True, blank=True, validators=[phone_regex])
    rengen_number = models.CharField(max_length=250, null=True, blank=True)
    patient_history = models.TextField(null=True, blank=True)

    def __str__(self):
        return str(self.first_name)

class Payments(models.Model):
    patient = models.ForeignKey(Patients, on_delete=models.CASCADE, related_name='payments')
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    amount = models.PositiveIntegerField(null=True, blank=True, default=0)
    PAYMENT_TYPE = (
        (NAQD, NAQD),
        (KARTA, KARTA),
    )
    payment_type = models.CharField(max_length=128, choices=PAYMENT_TYPE, default=NAQD)
    discount = models.IntegerField(default=0, null=True)

    @property
    def discount_amount(self):
        if self.discount:
            discount_percentage = self.discount / 100
            new_price = self.amount - (discount_percentage * self.amount)
            return new_price




