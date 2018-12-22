from rest_framework.views import APIView
from rest_framework.response import Response
from . import models, serializers


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
