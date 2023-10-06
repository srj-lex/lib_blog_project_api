from rest_framework import filters, mixins, permissions, viewsets
from rest_framework.pagination import LimitOffsetPagination

from posts.models import Comment, Follow, Group, Post

from . import serializers
from .permissions import AnonReadAuthReadAndWrite


class PostViewSet(viewsets.ModelViewSet):
    queryset = Post.objects.select_related("author")
    serializer_class = serializers.PostSerializer
    permission_classes = (AnonReadAuthReadAndWrite,)
    pagination_class = LimitOffsetPagination

    def perform_create(self, serializer):
        serializer.is_valid()
        serializer.save(author=self.request.user)


class CommentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.CommentSerializer
    permission_classes = (AnonReadAuthReadAndWrite,)

    def get_queryset(self):
        post_id = self.kwargs.get("post_id")
        qs = Comment.objects.filter(post=post_id).select_related("author")
        return qs

    def perform_create(self, serializer):
        serializer.is_valid()
        post = Post.objects.get(pk=self.kwargs.get("post_id"))
        serializer.save(author=self.request.user, post=post)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Group.objects.all()
    serializer_class = serializers.GroupSerializer


class FollowViewSet(mixins.CreateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    serializer_class = serializers.FollowSerializer
    permission_classes = (permissions.IsAuthenticated,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ("following__username",)

    def get_queryset(self):
        return Follow.objects.filter(user=self.request.user)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
