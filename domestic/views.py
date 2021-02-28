
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.conf import settings
from django.views.generic import FormView
from domestic.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render

from blog.models import Post
from domestic.models import Post_Domestic
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
from django.urls import reverse
from blog.models import Post
# Create your views here.

class PostLV(ListView):
    model = Post
    template_name = 'domestic/post_all.html'
    context_object_name = 'posts'
    paginate_by=10
    def get_queryset(self):
        return Post.objects.filter(category='D')
class PostDV(DetailView):
    model = Post
    def get_queryset(self):
        return Post.objects.filter(category='D')
    template_name='domestic/post_domestic_detail.html'
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['disqus_short'] = f"{settings.DISQUS_SHORTNAME}"
        context['disqus_id']= f"post-{self.object.id}-{self.object.slug}"
        context['disqus_url']=f"{settings.DISQUS_MY_DOMAIN}{self.object.get_absolute_url()}"
        context['disqus_title']=f"{self.object.slug}"
        return context

class PostAV(ArchiveIndexView):
    model = Post_Domestic
    date_field = 'modify_dt'

class PostYAV(YearArchiveView):
    model =Post_Domestic
    date_field = 'modify_dt'
    make_object_list= True

class PostMAV(MonthArchiveView) :
    model = Post_Domestic
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model = Post_Domestic
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView):
    model=Post_Domestic
    date_field = 'modify_dt'

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post_Domestic.objects.filter(tags__name=self.kwargs.get('tag'))
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tagname']= self.kwargs['tag']
        return context


class SearchFormView(FormView):
    form_class= PostSearchForm
    template_name= 'blog/post_search.html'

    def form_valid(self, form):
        searchWord = form.cleaned_data['search_word']
        post_list=Post.objects.filter(Q(title__icontains=searchWord) | Q(description__icontains=searchWord)|Q(content__icontains=searchWord)).distinct()
        context={}
        context['form']=form
        context['search_term']=searchWord
        context['object_list']= post_list

        return render(self.request, self.template_name, context) 

class PostCreateView(LoginRequiredMixin, CreateView):
    model =Post
    template_name='domestic/post_domestic_form.html'
    fields = ['title', 'content', 'tags', 'category']
    permission_denied_message='로그인이 필요합니다.'   
    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(PostCreateView,self).get_initial()
    # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['category'] = 'D'
       # etc...
        return initial
  
    
    def get_success_url(self):
        return reverse('domestic:post_detail', args=[self.object.pk])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)


class PostChangeLV(LoginRequiredMixin, ListView):
    template_name= 'domestic/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model= Post_Domestic
    fields= ['title', 'content', 'tags']
    success_url = reverse_lazy('domestic:index')

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model =Post_Domestic
    success_url = reverse_lazy('domestic:index')
