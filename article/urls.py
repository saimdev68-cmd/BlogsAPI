from rest_framework.routers import DefaultRouter
from django.urls import path
from .views import CategoryViewSet , ArticleViewSet , ParagraphViewSet , CommentViewSet , BookMarkView

router = DefaultRouter()
router.register("category",CategoryViewSet)
router.register("article",ArticleViewSet,basename="article")
router.register("paragraph",ParagraphViewSet,basename="paragraph")
router.register("comments",CommentViewSet,basename="comments")

urlpatterns = router.urls + [
    path("bookmark/",BookMarkView.as_view()),
]
