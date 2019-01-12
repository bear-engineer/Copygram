from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers
from rest_framework import status
from nomadgram.notifications import views as notification_views


class Feed(APIView):
    def get(self, request, format=None):
        # 요청을 보낸 유저
        user = request.user

        # 유저의 following 목록
        following_users = user.following.all()
        image_list = []

        # 유저의 following 중인 유저들의 포스트 목록을 불러온 후에 하나의 리스트로 합치기
        for following_user in following_users:
            image_list += following_user.images.all()[:2]

        # 최신 순으로정렬
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)
        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(data=serializer.data)


class LikeImage(APIView):
    def post(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            models.Like.objects.get(
                creator=request.user,
                image=found_image,
            )

            return Response(status=status.HTTP_304_NOT_MODIFIED)
        except models.Like.DoesNotExist:

            new_like = models.Like.objects.create(
                creator=user,
                image=found_image
            )
            new_like.save()

            notification_views.create_notification(user, found_image.creator, 'like', found_image)
            return Response(status=status.HTTP_201_CREATED)


class UnLikeImage(APIView):
    def delete(self, request, image_id, format=None):
        user = request.user

        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            preexisiting_like = models.Like.objects.get(
                creator=request.user,
                image=found_image,
            )
            preexisiting_like.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Like.DoesNotExist:
            return Response(status=status.HTTP_304_NOT_MODIFIED)


class CommentOnImage(APIView):
    def post(self, request, image_id, format=None):

        user = request.user
        try:
            found_image = models.Image.objects.get(id=image_id)
        except models.Image.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        serializer = serializers.CommentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(creator=user, image=found_image)
            notification_views.create_notification(
                user,
                found_image.creator,
                'comment',
                found_image,
                serializer.data['message']
            )
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(data=serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class Comment(APIView):
    def delete(self, request, comment_id, format=None):
        user = request.user

        try:
            comment = models.Comment.objects.get(id=comment_id, creator=user)
            comment.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)


class Search(APIView):
    def get(self, request, format=None):
        hashtags = request.query_params.get('hashtags', None)
        if not hashtags:
            return Response(status=status.HTTP_400_BAD_REQUEST, data='[?hashtags=tag] 형태로 검색을 권장합니다.')
        else:
            hashtags = hashtags.split(',')

            # .distinct() 중복된 결과값을 제거한다.
            images = models.Image.objects.filter(tags__name__in=hashtags).distinct()
            serializer = serializers.CountImageSerializer(images, many=True)
            return Response(data=serializer.data, status=status.HTTP_200_OK)


class ModeratedComments(APIView):
    """
    해당하는 image 의 owner 가 comments 를 지울수 있다.
    """
    def delete(self, request, image_id, comment_id, format=None):
        user = request.user
        # try:
        #     image = models.Image.objects.get(id=image_id, creator=user)
        # except models.Image.DoesNotExist:
        #     return Response(status=status.HTTP_404_NOT_FOUND)

        try:
            comment_to_delete = models.Comment.objects.get(
                id=comment_id,
                image__id=image_id,
                image__creator=user
            )
            comment_to_delete.delete()
        except models.Comment.DoesNotExist:
            return Response(status=status.HTTP_404_NOT_FOUND)

        return Response(status=status.HTTP_204_NO_CONTENT)
