from django.contrib.auth import get_user_model
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from nomadgram.notifications import views as notification_views
from . import models, serializers
from allauth.socialaccount.providers.facebook.views import FacebookOAuth2Adapter
from rest_auth.registration.views import SocialLoginView

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

        notification_views.create_notification(user, user_to_follow, 'follow')

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
    def get_user(self, username):
        try:
            found_user = models.User.objects.get(username=username)
            return found_user
        except models.User.DoesNotExist:
            return None

    def get(self, request, username, format=None):
        found_user = self.get_user(username)

        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.UserProfileSerializer(found_user)

        return Response(status=status.HTTP_200_OK, data=serializer.data)

    def put(self, request, username, format=None):
        found_user = self.get_user(username)
        user = request.user
        if found_user is None:
            return Response(status=status.HTTP_404_NOT_FOUND)
        elif found_user.username != user.username:
            return Response(status=status.HTTP_401_UNAUTHORIZED)
        serializer = serializers.UserProfileSerializer(found_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(data=serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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

        if not username:
            return Response(
                data='해당하는 유저가 존재하지 않거나 검색방법이 잘못되었습니다. [?username=username]',
                status=status.HTTP_400_BAD_REQUEST
            )
        users = models.User.objects.filter(username__istartswith=username)
        serializer = serializers.ListUserSerializer(users, many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)


class ChangePassword(APIView):
    def put(self, request, username, format=None):
        user = request.user
        current_password = request.data.get('current_password', None)
        new_password = request.data.get('new_password', None)

        if user.username != username:
            return Response(data="권한이 없습니다.", status=status.HTTP_401_UNAUTHORIZED)
        if current_password is not None:
            password_match = user.check_password(current_password)

            if password_match:
                if new_password is not None:
                    user.set_password(new_password)
                    user.save()
                    return Response(status=status.HTTP_200_OK)
                else:
                    return Response(status=status.HTTP_400_BAD_REQUEST)

            else:
                return Response(data="비밀번호가 일치하지 않습니다.", status=status.HTTP_400_BAD_REQUEST)


class FacebookLogin(SocialLoginView):
    adapter_class = FacebookOAuth2Adapter
