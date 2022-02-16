from django import forms

from .models import Post, Comment, Follow


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = (
            "text",
            "group",
            "image",
        )
        labels = {
            "text": "Текст поста",
            "group": "Группа",
            "image": "Картинка",
        }
        help_texts = {
            "text": "Текст нового поста",
            "group": "Группа, к которой будет относиться пост",
        }


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = {"text"}
        labels = {"text": "Текст"}


class FollowForm(forms.ModelForm):
    """Форма подписки на авторов."""

    class Meta:
        model = Follow
        fields = {"user"}
        labels = {"Пользователь подписывается на:"}
