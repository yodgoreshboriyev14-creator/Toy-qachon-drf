from django.contrib.auth.models import AbstractUser
from django.db.models.deletion import CASCADE
from django.db.models.enums import TextChoices
from django.db.models import CharField, BigIntegerField,  DateField, BooleanField, Model
from django.db.models.fields.related import ForeignKey

from apps.managers import UserManager


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

class Guests(Model):

    class SideType(TextChoices):
        BRIDGE = 'bridge', 'Kelin tomoni'
        GROOM = 'groom', 'Kuyov tomoni'

    class StatusType(TextChoices):
        INVITED = 'invited' , 'Taklif qilindi'
        CONFIRMED = 'confirmed' , 'Tasdiqlandi'
        DECLINED  = 'declined', 'Kelmaydi'

    class GroupType(TextChoices):
        FAMILY = 'family', 'Oila'
        FRIENDS = 'friends', 'Do`stlar'
        COLLEAGUES = 'colleagues', 'Hamkasblar'

    user = ForeignKey('apps.User', on_delete=CASCADE, related_name='guests')
    full_name = CharField(max_length=255)
    phone_number = CharField(max_length=20, blank=True)
    side = CharField(max_length=20, choices=SideType.choices)
    status = CharField(max_length=20, choices=StatusType.choices)
    group = CharField(max_length=20, choices=GroupType.choices)

    def __str__(self):
        return self.full_name



    



