from rest_framework.fields import CharField
from rest_framework.serializers import ModelSerializer

from apps.models import User


class RegisterModelSerializers(ModelSerializer):
    password = CharField(write_only=True)

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

