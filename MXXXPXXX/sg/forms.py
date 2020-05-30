from django import forms


class ArticleTitle(forms.Form):
    article_title = forms.CharField()