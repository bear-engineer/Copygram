from django.contrib.auth import get_user_model
from rest_framework import serializers
from . import models
from taggit_serializer.serializers import TagListSerializerField, TaggitSerializer

User = get_user_model()


class SmallImageSerializer(serializers.ModelSerializer):
    """
    Used fro tho notifications
    """

    class Meta:
        model = models.Image
        fields = (
            'file',
        )


class CountImageSerializer(TaggitSerializer, serializers.ModelSerializer):
    tags = TagListSerializerField()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'comment_count',
            'like_count',
            'tags'
        )


class FeedUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = (
            'username',
            'profile_image',
        )


class CommentSerializer(serializers.ModelSerializer):
    creator = FeedUserSerializer(read_only=True)

    class Meta:
        model = models.Comment
        fields = (
            'id',
            'message',
            'creator',
        )


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Like
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    comments = CommentSerializer(many=True)
    creator = FeedUserSerializer()

    class Meta:
        model = models.Image
        fields = (
            'id',
            'file',
            'location',
            'caption',
            'comments',
            'like_count',
            'creator',
            'created_at'

        )


class InputImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Image
        fields = (
            'file',
            'location',
            'caption',
        )
