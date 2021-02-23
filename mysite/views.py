from django.views.generic import TemplateView
from django.views.generic import CreateView
from django.contrib.auth.forms import UserCreationForm
from django.urls import reverse_lazy
from django.views.generic import ListView
from django.contrib.auth.mixins import AccessMixin
from blog.models import Post
from django.apps import apps
from domestic.models import Post_Domestic


class HomeView(ListView):
    template_name='home.html'
    model = Post
    context_object_name='posts'
    def get_queryset(self):
        return Post.objects.order_by('modify_dt')
    
    def get_context_data(self,**kwargs):
        context=super(HomeView, self).get_context_data(**kwargs)
        context['post_domestics'] = Post_Domestic.objects.order_by('modify_dt')
        return context



class UserCreateView(CreateView):
    template_name = 'registration/register.html'
    form_class = UserCreationForm
    success_url = reverse_lazy('register_done')

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