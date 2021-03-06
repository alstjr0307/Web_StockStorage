from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib import messages
from django.contrib.auth import authenticate
from blog.models import PostComment

from django.contrib.auth.forms import AuthenticationForm

class UserCreationForm(UserCreationForm):
  
    error_messages = {
        'password_mismatch': "비밀번호가 일치하지 않습니다",
        'password_common': "비밀번호가 너무 간단합니다",
    } 
    first_name= forms.CharField(label='닉네임',max_length=7, min_length=2, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control', 'placeholder':'2~7자 이내로 입력 가능합니다.'})))
    username= forms.CharField(label='아이디',max_length=10, min_length=2, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control','placeholder':'2~10자 이내로 입력 가능합니다.'})))
    email= forms.EmailField(label='이메일', required=True, widget=(forms.EmailInput(attrs={'class': 'form-control'})))
    
    class Meta:
        model = User
        fields = ("username",  "email", "password1", "password2","first_name")
        labels = {
        'username': '아이디',
        'email': '이메일',
        'first_name':'닉네임'
        }

        error_messages = {
            'username': {
                'unique': '아이디가 중복됩니다',
            },
            'email': {
                'unique': '이메일이 중복됩니다',
                'invalid': '잘못된 이메일입니다',
            },
            'first_name':{
                'unique': '닉네임이 중복됩니다',
            }
        }

    def clean_email(self):
        data = self.cleaned_data['email']
        if User.objects.filter(email=data).exists():
            raise forms.ValidationError("사용중인 이메일입니다")
        return data

    def clean_username(self):
        data = self.cleaned_data['username']
        if User.objects.filter(username=data).exists():
            raise forms.ValidationError("사용중인 아이디입니다")
        return data

    def clean_first_name(self):
        dat = self.cleaned_data['first_name']
        
        if User.objects.filter(first_name=dat).exists():
            raise forms.ValidationError("사용중인 닉네임입니다")
        return dat



class ProfileForm(forms.ModelForm):
    first_name= forms.CharField(label='닉네임',max_length=7, min_length=2, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))
    
    class Meta:
        model = User
        fields = [
            'first_name',
            ]
    def clean_first_name(self):
        dat = self.cleaned_data['first_name']
        
        if User.objects.filter(first_name=dat).exists():
            raise forms.ValidationError("사용중인 닉네임입니다")
        return dat



class CustomLoginRequiredMixin(LoginRequiredMixin):

    permission_denied_message='로그인이 필요합니다.'
    login_url = 'login'
    def dispatch(self, request, *args, **kwargs):
        if not request.user.is_authenticated:
            messages.add_message(request, messages.WARNING, self.permission_denied_message)
            return self.handle_no_permission()
        return super(CustomLoginRequiredMixin, self).dispatch(request, *args, **kwargs
    )


class CustomAuthenticationForm(AuthenticationForm):
    username= forms.CharField(label='아이디',max_length=10, min_length=2, required=True,
                               widget=(forms.TextInput(attrs={'class': 'form-control'})))

    error_messages = {
        'invalid_login': (
            "비밀번호나 아이디가 틀립니다"
        ),
        'inactive': ("이 계정은 인증되지 않았습니다. 인증을 먼저 진행해 주세요."),


    }

    def __init__(self, request=None, *args, **kwargs):
        super(CustomAuthenticationForm, self).__init__(*args, **kwargs) # 꼭 있어야 한다!

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        if username is not None and password:
            self.user_cache = authenticate(self.request, username=username, password=password)
            if self.user_cache is None:
                try:
                    user_temp = User.objects.get(username=username)
                except:
                    user_temp = None

                if user_temp is not None:
                        self.confirm_login_allowed(user_temp)
                else:
                    raise forms.ValidationError(
                        self.error_messages['invalid_login'],
                        code='invalid_login',
                        params={'username': self.username_field.verbose_name},
                    )

        return self.cleaned_data


class NewCommentForm(forms.ModelForm):
    class Meta:
        model = PostComment
        fields = ['content', 'blogpost_connected']

