from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

from . import models, serializers

User = get_user_model()


class ExploreUsers(APIView):
    def get(self, request, format=None):
        last_five = models.User.objects.all().order_by('-date_joined')[:5]
        serializer = serializers.ListUserSerializer(last_five, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class FollowUser(APIView):
    def post(self, request, user_id, format=None):
        user = request.user
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.following.add(user_to_follow)
        user.save()
        return Response(status=status.HTTP_200_OK)


class UnFollowUser(APIView):
    def post(self, request, user_id, format=None):
        user = request.user
        try:
            user_to_follow = models.User.objects.get(id=user_id)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user.following.remove(user_to_follow)
        user.save()
        return Response(status=status.HTTP_200_OK)


class UserProfile(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(status=status.HTTP_200_OK, data=serializer.data)


class UserFollowers(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)
        user_followers = found_user.followers.all()
        serializer = serializers.ListUserSerializer(user_followers, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class UserFollowing(APIView):
    def get(self, request, username, format=None):
        try:
            found_user = models.User.objects.get(username=username)
        except models.User.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        user_following = found_user.following.all()

        serializer = serializers.ListUserSerializer(user_following, many=True)

        return Response(data=serializer.data, status=status.HTTP_200_OK)


class Search(APIView):
    def get(self, request, format=None):
        username = request.query_params.get('username', None)
        users = models.User.objects.filter(username__icontains=username)
        if not users:
            return Response(
                data='해당하는 유저가 존재하지 않거나 검색방법지 잘못되었습니다.\n[?username=username]',
                status=status.HTTP_400_BAD_REQUEST
            )
        serializer = serializers.ListUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)
