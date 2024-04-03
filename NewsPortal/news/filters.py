from django.forms import DateTimeInput
from django_filters import FilterSet, ModelChoiceFilter, DateTimeFilter, CharFilter, ChoiceFilter
from .models import Post, Category


class PostFilter(FilterSet):
    postCategory = ModelChoiceFilter(
        # field_name='postCategory',
        queryset=Category.objects.all(),
        label='По категории',
        empty_label='без фильтра',
        # conjoined=True,
    )

    title = CharFilter(
        label='По заголовоку новости',
        lookup_expr='iregex'
    )

    categoryType = ChoiceFilter(
        empty_label='без фильтра',
        label='По типу публикации',
        choices=Post.CATEGORY_CHOICES
    )

    added_after = DateTimeFilter(
        label='По дате',
        field_name='dateCreation',
        lookup_expr='gt',
        widget=DateTimeInput(
            format='%Y-%m-%dT%H:%M',
            attrs={'type': 'datetime-local'},
        ),
    )
