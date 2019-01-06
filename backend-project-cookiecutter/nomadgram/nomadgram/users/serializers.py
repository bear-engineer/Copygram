from django.contrib.auth import get_user_model
from rest_framework import serializers

User = get_user_model()


class ExploreUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'id',
            'profile_image',
            'username',
            'name'
        )
