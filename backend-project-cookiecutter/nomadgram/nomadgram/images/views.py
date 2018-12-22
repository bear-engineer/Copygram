from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class ListAllImages(APIView):
    def get(self, request, format=None):

        # 현재 요청을 보낸 유저가 http/https 를 사용하는지에 대한 판별
        print(request.scheme)
        # 현재 요청을 보낸 유저가 followers 하는 유저
        print(request.user.followers)
        all_images = models.Image.objects.all()
        serializer = serializers.ImageSerializer(all_images, many=True)
        return Response(data=serializer.data)


class ListAllComment(APIView):
    def get(self, request, format=None):
        all_comments = models.Comment.objects.all()
        serializer = serializers.CommentSerializer(all_comments, many=True)
        return Response(data=serializer.data)


class ListAllLikes(APIView):
    def get(self, request, format=None):
        all_likes = models.Like.objects.all()
        serializer = serializers.LikeSerializer(all_likes, many=True)
        return Response(data=serializer.data)
