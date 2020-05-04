from django import forms


class KeywordForm(forms.Form):
    keyword_text = forms.CharField()
