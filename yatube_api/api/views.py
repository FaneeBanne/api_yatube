from rest_framework import viewsets
from django.shortcuts import get_object_or_404
from rest_framework.exceptions import PermissionDenied


from posts.models import Post, Group, Comment
from api.serializers import PostSerializer, GroupSerializer, CommentSerializer


RAISE_403 = PermissionDenied('Редактирование чужих данных запрещено!')


class PostViewSet(viewsets.ModelViewSet):
      queryset = Post.objects.all()
      serializer_class = PostSerializer

      def perform_create(self, serializer):
            serializer.save(author=self.request.user)

      def perform_update(self, serializer):
            if serializer.instance.author != self.request.user:
                  raise RAISE_403
            super().perform_update(serializer)

      def perform_destroy(self, instance):
            if instance.author != self.request.user:
                  raise RAISE_403
            instance.delete()


class GroupViewSet(viewsets.ReadOnlyModelViewSet):
      queryset = Group.objects.all()
      serializer_class = GroupSerializer


class CommentsViewSet(viewsets.ModelViewSet):
      serializer_class = CommentSerializer

      def get_queryset(self):
            post_id = self.kwargs.get("post_id")
            new_queryset = Comment.objects.filter(post=post_id)
            return new_queryset

      def perform_create(self, serializer):
            post = get_object_or_404(Post, id=self.kwargs.get('post_id'))
            serializer.save(author=self.request.user, post=post)

      def perform_update(self, serializer):
            if serializer.instance.author != self.request.user:
                  raise RAISE_403
            super().perform_update(serializer)

      def perform_destroy(self, instance):
            if instance.author != self.request.user:
                  raise RAISE_403
            instance.delete()

