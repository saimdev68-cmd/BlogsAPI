from rest_framework import serializers
from .models import Category , Article , Paragraph , Comment

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ["id","name","slug"]
        read_only_fields = ["slug"]

class ArticleSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        fields = ["id",
                "category",
                "title",
                "description",
                "cover_image",
                "read_min",
                "likes_count",
                "comments_count"
                ]

class ArticleAdminSerializer(serializers.ModelSerializer):
    likes_count = serializers.IntegerField(read_only=True)
    comments_count = serializers.IntegerField(read_only=True)
    bookmark_count = serializers.IntegerField(read_only=True)
    class Meta:
        model = Article
        fields = ["id",
                "category",
                "title",
                "description",
                "cover_image",
                "read_min",
                "is_published",
                "published_at",
                "is_top",
                "is_trending",
                "bookmark",
                "likes",
                "likes_count",
                "comments_count",
                "bookmark_count"
                ]
    
class ParagraphSerializer(serializers.ModelSerializer):
    class Meta:
        model = Paragraph
        fields = ["id","article","heading","description","index"]
    
class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ["id","article","profile","text"]
        read_only_fields = ["profile"]

    def validate(self, attrs):
        profile = self.context.get("request").user.profile
        article = attrs.get("article")
        if Comment.objects.filter(article=article,profile=profile).exists():
            raise serializers.ValidationError("You Already comment on this article")
        return attrs