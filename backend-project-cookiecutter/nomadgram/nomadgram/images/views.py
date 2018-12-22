from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


class Feed(APIView):
    def get(self, request, format=None):
        user = request.user
        following_users = user.following.all()

        # [item.images.all()[:2] for item in following_users]
        image_list = []

        # list 추출
        for following_user in following_users:
            image_list += following_user.images.all()[:2]

        # 정렬
        sorted_list = sorted(image_list, key=lambda image: image.created_at, reverse=True)

        serializer = serializers.ImageSerializer(sorted_list, many=True)

        return Response(data=serializer.data)


