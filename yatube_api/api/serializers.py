from rest_framework import serializers

from posts.models import Comment, Group, Post


class GroupSerializer(serializers.ModelSerializer):
    """Сериализатор для работы с моделями тематических групп."""

    class Meta:
        """Мета-параметры сериализатора групп."""

        model = Group
        fields = ('id', 'title', 'slug', 'description')


class PostSerializer(serializers.ModelSerializer):
    """Сериализатор для создания, редактирования и чтения публикаций."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)

    class Meta:
        """Мета-параметры сериализатора публикаций."""

        model = Post
        fields = ('id', 'text', 'pub_date', 'author', 'image', 'group')


class CommentSerializer(serializers.ModelSerializer):
    """Сериализатор для управления комментариями к публикациям."""

    author = serializers.SlugRelatedField(slug_field='username',
                                          read_only=True)
    post = serializers.PrimaryKeyRelatedField(read_only=True)

    class Meta:
        """Мета-параметры сериализатора комментариев."""

        model = Comment
        fields = ('id', 'author', 'post', 'text', 'created')
