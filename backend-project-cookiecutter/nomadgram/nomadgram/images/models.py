from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class TimeStampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    # field 가 아닌 extra
    class Meta:
        # 해당 model 을 database 에 연결하지 않고 다른 model 에 상속하여 사용한다.
        abstract = True


class Image(TimeStampedModel):
    """
    Image Model
    """
    file = models.ImageField()
    location = models.CharField(max_length=140)
    caption = models.TextField()
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='images',
        null=True
    )

    @property
    def like_count(self):
        return self.likes.all().count()

    def __str__(self):
        return f'{self.location} - {self.caption}'

    class Meta:
        ordering = ['-created_at']


class Comment(TimeStampedModel):
    """
    Comment Model
    """
    message = models.TextField()
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='comments',
        null=True
    )

    def __str__(self):
        return f'{self.message} - {self.creator}'


class Like(TimeStampedModel):
    """
    Like Model
    """
    creator = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True
    )
    image = models.ForeignKey(
        Image,
        on_delete=models.CASCADE,
        related_name='likes',
        null=True
    )

    def __str__(self):
        return f'{self.image.creator} 님의 글 {self.image.caption} 을(를) {self.creator} 님이 좋아합니다!'
