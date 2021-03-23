from django import forms
from .models import Post
from taggit.forms import TagWidget
from froala_editor.widgets import FroalaEditor

class PostSearchForm(forms.Form):
    search_word = forms.CharField(label='검색',min_length=1)



class PostForm(forms.ModelForm):
  class Meta:
    model= Post
    fields=['title', 'content', 'tags']
    widgets = {
      'tags': TagWidget(),
    }



  