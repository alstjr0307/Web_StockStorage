from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
    

    email = forms.EmailField(label='이메일',required=True, widget=(forms.TextInput(attrs={'class': 'form-control'})))
    nickname = forms.CharField(label= '닉네임',max_length=6, min_length=2, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder':'2자~6자까지 가능합니다.'})))
    
    class Meta:
        model = User
        fields = ("username",  "email", "password1", "password2","nickname")
        labels = {
        'username': '아이디',
        'email': '이메일',
        }
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
        }


    def save(self, commit=True):
        user = super(UserCreationForm, self).save(commit=False)
        user.first_name=self.cleaned_data["nickname"]
       
        if commit:
            user.save()
        return user

class ProfileForm(forms.ModelForm):
    first_name= forms.CharField(label='닉네임',max_length=12, min_length=2, required=True, help_text='Required: Nickname',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    
    
    class Meta:
        model = User
        fields = [
            'username',
            'first_name',
            'email',
            ]