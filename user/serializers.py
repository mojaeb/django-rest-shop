from django.core.validators import RegexValidator
from rest_framework import serializers
from .models import CustomUser


class CustomUserSerializer(serializers.ModelSerializer):
    """
    Currently unused in preference of the below.
    """
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Phone number must be entered in the format: '+999999999'. Up to 15 digits "
                                         "allowed.")
    phone_number = serializers.CharField(validators=[phone_regex], required=True)
    email = serializers.EmailField(required=True)
    first_name = serializers.CharField(required=True)
    password = serializers.CharField(min_length=8, write_only=True)
    last_name = serializers.CharField(required=True)
    user_name = serializers.CharField(required=True)

    class Meta:
        model = CustomUser
        fields = ('phone_number', 'email', 'first_name', 'last_name', 'password', 'user_name')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        # as long as the fields are the same, we can just use this
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance
