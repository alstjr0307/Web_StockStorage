from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    email = forms.EmailField(label='이메일',required=True)
    nickname = forms.CharField(label= '닉네임',max_length=12, min_length=2, required=True, help_text='Required: Nickname',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))


    class Meta:
        model = User
        fields = ("username", "nickname", "email", "password1", "password2",)

    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.email = self.cleaned_data["email"]
        user.first_name=self.cleaned_data["nickname"]
       
        if commit:
            user.save()
        return user