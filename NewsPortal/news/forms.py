from django import forms
from django.core.exceptions import ValidationError

from .models import Post, Category, Author


class PostForm(forms.ModelForm):
    author = forms.ModelChoiceField(
        label='Автор',
        queryset=Author.objects.all()
    )
    # categoryType = forms.ChoiceField(
    #     label='Тип публикации',
    #     choices=Post.CATEGORY_CHOICES,
    # )
    postCategory = forms.ModelMultipleChoiceField(
        label='Категория',
        queryset=Category.objects.all(),
    )
    title = forms.CharField(label='Заголовок', widget=forms.TextInput(attrs={'class': 'form-control'}))
    text = forms.CharField(min_length=20, label='Текст публикации', widget=forms.Textarea)

    class Meta:
        model = Post
        fields = ['author', 'postCategory', 'title', 'text']

    def clean(self):
        cleaned_data = super().clean()
        title = cleaned_data.get("title")
        text = cleaned_data.get("text")

        if title == text:
            raise ValidationError(
                "Заголовок не должен быть одинаковым с текстом новости"
            )

        return cleaned_data
