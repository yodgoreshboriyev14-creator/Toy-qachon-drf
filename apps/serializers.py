from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import User, Guests


class RegisterModelSerializers(ModelSerializer):
    password = CharField(write_only=True, min_length=4)


    class Meta:
        model = User
        fields = 'phone_number' , 'password'

    def create(self, validated_data):
        return User.objects.create_user(**validated_data)


class UserModelSerializers(ModelSerializer):
    class Meta:
        model = User
        fields = 'id', 'phone_number', 'language', 'wedding_day', 'premium_status', 'telegram_id'
        read_only_fields = ['id']

class GuestModelSerializer(ModelSerializer):
    class Meta:
        model = Guests
        fields = ['id', 'full_name', 'phone_number', 'side', 'status', 'group']
        read_only_field = ['id']



