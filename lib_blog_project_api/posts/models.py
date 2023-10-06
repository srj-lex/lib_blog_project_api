from django.contrib.auth import get_user_model
from django.db import models


User = get_user_model()

CHARS_IN_STR = 15


class Post(models.Model):
    text = models.TextField("Текст поста", )
    pub_date = models.DateTimeField("Дата публикации", auto_now_add=True)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="posts"
    )
    image = models.ImageField(upload_to="posts/", null=True, blank=True)
    group = models.ForeignKey(
        "Group",
        on_delete=models.SET_NULL,
        related_name="posts",
        blank=True,
        null=True,
    )

    def __str__(self) -> str:
        return self.text[:CHARS_IN_STR]


class Comment(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comments"
    )
    post = models.ForeignKey(
        Post, on_delete=models.CASCADE, related_name="comments"
    )
    text = models.TextField("Текст комментария", )
    created = models.DateTimeField(
        "Дата добавления", auto_now_add=True, db_index=True
    )

    def __str__(self) -> str:
        return self.text[:CHARS_IN_STR]


class Group(models.Model):
    title = models.CharField("Заголовок группы", max_length=200)
    slug = models.SlugField("Адрес", unique=True)
    description = models.TextField("Описание", )

    def __str__(self) -> str:
        return self.title


class Follow(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="user",
    )

    following = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="following",
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "following"], name="uq_user_following"
            )
        ]

    def __str__(self) -> str:
        return self.author.username
