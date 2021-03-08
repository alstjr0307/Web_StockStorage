from django import forms
from blog.models import Post

from froala_editor.widgets import FroalaEditor
class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='검색')


class PostForm(forms.ModelForm):
  content = forms.CharField(widget=FroalaEditor)
  