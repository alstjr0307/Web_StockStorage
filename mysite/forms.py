from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class UserCreationForm(UserCreationForm):
<<<<<<< HEAD
    
=======
    email = forms.EmailField(label='이메일',required=True)
    nickname = forms.CharField(label= '닉네임',max_length=12, min_length=2, required=True, help_text='Required: Nickname',
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    labels = {
        'username': '닉네임',
        'email': '이메일',
        'password': '패스워드'
    }
>>>>>>> f64f7a8d0b9819a4a2822b323c99e833a7085ee2

    email = forms.EmailField(label='이메일',required=True, widget=(forms.TextInput(attrs={'class': 'form-control'})))
    nickname = forms.CharField(label= '닉네임',max_length=6, min_length=2, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder':'2자~6자까지 가능합니다.'})))
    
    class Meta:
        model = User
        fields = ("username",  "email", "password1", "password2","nickname")
        labels = {
        'username': '아이디',
        'email': '이메일',
        'password1': '패스워드',
        'password2': '패스워드 확인',
        }
        widgets = {
        'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder':'15자 이내로 입력 가능합니다.'}),
        'password1' : forms.PasswordInput(attrs={'class': 'form-control'}),
        'password2' : forms.PasswordInput(attrs={'class': 'form-control'}),
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