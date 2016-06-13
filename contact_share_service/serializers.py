from rest_framework import serializers
from rest_framework.validators import UniqueValidator

from contact_share_service.models import User, Card


class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        required=True,
        validators=[UniqueValidator(queryset=User.objects.all())])
    password = serializers.CharField(write_only=True)
    full_name = serializers.CharField(required=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'full_name', )


class CardSerializer(serializers.ModelSerializer):

    class Meta:
        model = Card
        fields = (
            'id',
            'owner',
            'name',
            'address',
            'job_title',
            'contact_number',
            'email',
            'organization',
            'image'
        )
