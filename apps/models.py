from django.contrib.auth.models import AbstractUser, UserManager
from django.db.models.enums import TextChoices
from django.db.models  import CharField, BigIntegerField, DateTimeField, DateField, BooleanField


# Create your models here.

class User(AbstractUser):
    class LanguageType(TextChoices):
        UZ_LATIN = "uz_latin", "O'zbek (lotin)"
        UZ_CYRILLIC = "uz_cyrillic", "O'zbek (Krill)"
        RU = "ru", "Rus"

    username = None
    phone_number = CharField(max_length=255, unique=True)
    telegram_id = BigIntegerField(null=True, blank=True, unique=True)
    language = CharField(max_length=15, choices=LanguageType, default=LanguageType.UZ_LATIN)
    wedding_day = DateField(null=True, blank=True)
    premium_status = BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'phone_number'
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.phone_number

    



