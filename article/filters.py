import django_filters
from .models import Article

class CategoryFilter(django_filters.FilterSet):
    other = django_filters.BooleanFilter(field_name="category",lookup_expr="isnull")

    class Meta:
        model = Article
        fields = ["category","other"]