from django import forms
from  .models import Post


class NewPostForm(forms.ModelForm):
    image = forms.ImageField(required=False ,label='add image to showcase in home feeds')
    class Meta:
        model = Post
        fields = ['title','image','content']