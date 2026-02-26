from django import forms
from .models import Comment, Post

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('author', 'text_comment')
        
class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('author_name', 'title', 'text') 
        widgets = {
            'author_name': forms.TextInput(attrs={'placeholder': 'Ваше имя'}),
            'title': forms.TextInput(attrs={'placeholder': 'Заголовок поста'}),
            'text': forms.Textarea(attrs={ 'placeholder': 'О чем хотите рассказать?'}),
        }