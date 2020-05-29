from django import forms
from .models import Article


class ArticleForm(forms.ModelForm):
    class Meta:
        model = Article
        fields = [
            'title',
            'keyword',
        ]


class ArticleTitle(forms.Form):
    article_title = forms.CharField()