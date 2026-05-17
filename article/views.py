from .models import Category , Article , Paragraph , Comment
from .permissions import CommentPermission
from .serializers import CategorySerializer , ArticleSerializer , ParagraphSerializer , CommentSerializer , ArticleAdminSerializer
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser , AllowAny , IsAuthenticated
from django.db.models import Count
from django_filters.rest_framework import DjangoFilterBackend
from .filters import CategoryFilter
from rest_framework import filters , generics
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404

# Create your views here.

class CategoryViewSet(ModelViewSet):
    serializer_class = CategorySerializer
    queryset = Category.objects.all()

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]

class ArticleViewSet(ModelViewSet):
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["title","category__name"]
    ordering_fields = ["published_at"]
    filterset_class = CategoryFilter

    def get_serializer_class(self):
        user = self.request.user
        if user.is_staff:
            return ArticleAdminSerializer
        return ArticleSerializer
    
    def get_queryset(self):
        user = self.request.user
        articles = Article.objects.all().annotate(
                likes_count=Count("likes",distinct=True),
                comments_count=Count("comments",distinct=True),
                bookmark_count = Count("bookmark",distinct=True)
            )
        if user.is_staff:
            return articles
        return articles.filter(is_published=True)
    
    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
    
    @action(detail=True,methods=['POST'],permission_classes=[IsAuthenticated])
    def like(self,request,pk):
        profile = request.user.profile
        article = get_object_or_404(Article,pk=pk)
        if article.likes.filter(id=profile.id).exists():
            article.likes.remove(profile)
            return Response ({"detail":"You Unlike this article"})
        else:
            article.likes.add(profile)
            return Response ({"detail":"You like this article"})
        
    @action(detail=True,methods=['POST'],permission_classes=[IsAuthenticated])
    def bookmark(self,request,pk):
        profile = request.user.profile
        article = get_object_or_404(Article,pk=pk,is_published=True)
        if article.bookmark.filter(id=profile.id).exists():
            article.bookmark.remove(profile)
            return Response ({"detail":"You unbookmark this article"})
        else:
            article.bookmark.add(profile)
            return Response ({"detail":"You bookmark this article"})
        
class BookMarkView(generics.ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = ArticleSerializer
    
    def get_queryset(self):
        return Article.objects.filter(bookmark=self.request.user.profile)
    
class ParagraphViewSet(ModelViewSet):
    serializer_class = ParagraphSerializer
    filter_backends = [DjangoFilterBackend,filters.SearchFilter,filters.OrderingFilter]
    search_fields = ["heading","article__title"]
    filterset_fields = ["article"]
    ordering_fields = ["id","index"]
    
    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Paragraph.objects.all()
        return Paragraph.objects.filter(article__is_published=True)

    def get_permissions(self):
        if self.action in ["list","retrieve"]:
            return [AllowAny()]
        return [IsAdminUser()]
    
class CommentViewSet(ModelViewSet):
    serializer_class = CommentSerializer
    permission_classes = [CommentPermission]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ["profile","article"]

    def perform_create(self, serializer):
        serializer.save(profile=self.request.user.profile)

    def get_queryset(self):
        user = self.request.user
        if user.is_staff:
            return Comment.objects.all()
        return Comment.objects.filter(article__is_published=True)