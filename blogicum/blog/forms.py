from django import forms
from django.utils.timezone import now

from .models import Post, Comment


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        exclude = ('author',)

        widgets = {
            'text': forms.Textarea({'rows': '5'}),
            'pub_date': forms.DateTimeInput(attrs={'type': 'datetime-local'},
                                            format='%Y-%m-%dT%H:%M')
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['pub_date'].initial = now()


class CommentForm(forms.ModelForm):

    class Meta:
        model = Comment
        fields = ('text',)

        widgets = {'text': forms.Textarea({'rows': '5'})}
