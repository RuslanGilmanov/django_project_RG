from django import forms
from .models import Post, Image
from django.forms import inlineformset_factory


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'content', 'tags']


class ImageForm(forms.ModelForm):
    class Meta:
        model = Image
        fields = ['image']


ImageFormSet = inlineformset_factory(Post, Image, form=ImageForm, extra=3, can_delete=True)
