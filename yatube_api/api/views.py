from django.shortcuts import get_object_or_404
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from posts.models import Group, Post
from .serializers import PostSerializer, GroupSerializer, CommentSerializer
from .permissions import IsAuthorOrReadOnly


class PostViewSet(viewsets.ModelViewSet):
    """Вьюсет для создания, редактирования, удаления и чтения публикаций."""

    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def perform_create(self, serializer):
        """Автоматически сохраняет текущего пользователя как автора поста."""
        serializer.save(author=self.request.user)


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
    """Вьюсет только для чтения информации о тематических группах."""

    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = (IsAuthenticated,)


class CommentViewSet(viewsets.ModelViewSet):
    """Вьюсет для управления комментариями к публикациям."""

    serializer_class = CommentSerializer
    permission_classes = (IsAuthenticated, IsAuthorOrReadOnly)

    def get_post(self):
        """Возвращает объект поста по его идентификатору из URL."""
        return get_object_or_404(Post, pk=self.kwargs.get('post_id'))

    def get_queryset(self):
        """Возвращает список комментариев, привязанных к конкретному посту."""
        post = self.get_post()
        return getattr(post, 'comments').all()

    def perform_create(self, serializer):
        """Автоматически связывает комментарий с его автором и постом."""
        serializer.save(author=self.request.user, post=self.get_post())
