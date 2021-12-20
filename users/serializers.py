from django.contrib.auth.models import User
from rest_framework.serializers import ModelSerializer, ReadOnlyField


class UserSerializer(ModelSerializer):
    date_joined = ReadOnlyField()

    class Meta:
        model = User
        fields = [
            'id',
            'username',
            'first_name',
            'last_name',
            'date_joined',
            'email',
            'password',
        ]
        extra_kwargs = {
            'password': {'write_only': True}
        }

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
