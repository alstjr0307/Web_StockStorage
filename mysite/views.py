from django.views.generic import TemplateView
from django.views.generic import CreateView, UpdateView
from blog.forms import PostSearchForm, PostForm
from django.views.generic import ListView, View, FormView
from django.contrib.auth.mixins import AccessMixin
from blog.models import Post
from django.db.models import Q
from .forms import UserCreationForm, ProfileForm
from datetime import datetime
from django.urls import reverse_lazy
from django.contrib.auth.models import User
from django.contrib.auth import views as auth_view
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from mysite.tokens import account_activation_token
from django.shortcuts import render, redirect
from django.utils.encoding import force_text
from django.contrib.auth import login
from .forms import CustomAuthenticationForm
from bs4 import BeautifulSoup
from urllib.request import Request, urlopen
from blog.forms import PostSearchForm
import math
from django.utils import timezone
from yahoo_fin import stock_info as si


class HomeView(ListView):
    template_name='home.html'
    model = Post
    context_object_name='posts'
    paginate_by=20

    def get_queryset(self):
        return Post.objects.order_by('-create_dt')
    def get_context_data(self,*args,**kwargs):
        context=super(HomeView, self).get_context_data(*args,**kwargs)
        data=[]
        f=open('/srv/django/price.txt', 'r')
        a=f.read()
        data=a.split(" ")     
        context['nasdaq']= data[6]
        context['kospi'] = data[0]
        context['kosdaq'] = data[3]
        context['time'] = data[7]

        context['kospi_df']= str(data[1]+data[2])
        context['kosdaq_df']=str(data[4]+data[5])
        context['nasdaq_df'] = data[7]+data[8]
        Post_Domestic=Post.objects.filter(category='D')
        Post_Foreign=Post.objects.filter(category='F')
        context['post_domestics'] = Post_Domestic.order_by('-create_dt')
        context['post_foreigns']=Post_Foreign.order_by('-create_dt')
        return context
    


##회원가입VIEW
class SignUp(CreateView):
    ##form은 forms.py에서 만든 UserCreationForm변형을 이용
    form_class = UserCreationForm
    ##template은 register.html
    template_name = 'registration/register.html'
    
    def get(self, request, *args, **kwargs):
        form = self.form_class()
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)
        if form.is_valid():

            user = form.save(commit=False)
            
            user.is_active = False # Deactivate account till it is confirmed
            user.save()

            current_site = get_current_site(request)
            subject = '주식저장소 가입 인증'
            message = render_to_string('registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject, message)

            messages.error(request,('가입 완료를 위해 이메일 인증을 해주세요'))

            return redirect('register_done')

        return render(request, self.template_name, {'form': form})
class UserCreateDoneTV(TemplateView):
    template_name = 'registration/register_done.html' 



class OwnerOnlyMixin(AccessMixin):
    raise_exception = True
    permission_denied_message = "게시물 작성자만 수정/삭제 가능합니다"
    
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj.owner:
            return self.handle_no_permission()

        return super().dispatch(request, *args,**kwargs)
    
class ProfileView(AccessMixin, UpdateView):
    model = User
    form_class = ProfileForm
    success_url = reverse_lazy('home')
    template_name='registration/profile.html'
    def dispatch(self, request, *args, **kwargs):
        obj = self.get_object()
        if request.user != obj:
            return self.handle_no_permission()

        return super().dispatch(request, *args,**kwargs)
    
class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True
            
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')

class CustomLoginView(auth_view.LoginView):
    form_class = CustomAuthenticationForm

class SearchFormView(FormView,ListView):
    form_class= PostSearchForm
    template_name= 'post_search.html'
    paginate_by=20
    model=Post.objects.all()
    def get_queryset(self):
        if self.request.method== "GET" and self.request.GET:
            query = self.request.GET.get("search_word")
            return Post.objects.filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()

        else: return []


    def get_context_data(self, **kwargs):

        context= super().get_context_data(**kwargs)
        context['search_word']= self.request.GET.get("search_word")
        return context


class FilteredListView(ListView):
    filterset_class = None

    def get_queryset(self):
        # Get the queryset however you usually would.  For example:
        queryset = super().get_queryset()
        # Then use the query parameters and the queryset to
        # instantiate a filterset and save it as an attribute
        # on the view instance for later.
        self.filterset = self.filterset_class(self.request.GET, queryset=queryset)
        # Return the filtered queryset
        return self.filterset.qs.distinct()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # Pass the filterset to the template - it provides the form.
        context['filterset'] = self.filterset
        return context