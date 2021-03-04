
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView

from django.views.generic.list import MultipleObjectMixin
from django.conf import settings
from django.views.generic import FormView
from domestic.forms import PostSearchForm
from django.db.models import Q
from django.shortcuts import render
from django.core.paginator import Paginator
from blog.models import Post, PostComment
from mysite.forms import CustomLoginRequiredMixin, NewCommentForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin, FilteredListView
from django.urls import reverse
from blog.models import Post
from django.views.generic.edit import FormMixin
from django.shortcuts import get_object_or_404
# Create your views here.

class PostLV(ListView,FormView):
    
    form_class= PostSearchForm
    template_name = 'domestic/post_all.html'
    context_object_name = 'posts'
    paginate_by=20
    model=Post
    def get_queryset(self):
        return Post.objects.filter(category='D')


class PostDV(DetailView, FormView, MultipleObjectMixin,FormMixin):

    template_name='domestic/post_domestic_detail.html'
    model = Post
    paginate_by=20
    form_class= NewCommentForm
    def get_success_url(self):	# post처리가 성공한뒤 행할 행동
        return reverse('domestic:post_detail', kwargs={'pk': self.object.pk})
    def get_queryset(self):
        return Post.objects.filter(category='D')

    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
        comments_connected = PostComment.objects.filter(blogpost_connected=self.get_object()).order_by('created')
        context['comments'] = comments_connected

        context['user'] = self.request.user
        
        context['posts'] = Post.objects.filter(category='D')
        if self.request.user.is_authenticated:
            context['comment_form'] = '1'

        return context


    def post(self, request, *args, **kwargs):
        self.object= self.get_object()
        form = self.get_form()		# form데이터 받아오기	

        if form.is_valid():			# form의 내용이 정상적일 경우
            return self.form_valid(form)	#form_valid함수 콜
        else:			
            return self.form_invalid(form)

    def form_valid(self, form):	# form_valid함수
        comment = form.save(commit=False)	# form데이터를 저장. 그러나 쿼리실행은 x
        comment.blogpost_connected = get_object_or_404(Post, pk=self.object.pk) # photo object를 call하여 photocomment의 photo로 설정(댓글이 속할 게시글 설정) pk로 pk설정 pk - photo id 
        comment.writer = self.request.user
        # 댓글쓴 사람 설정. 
        comment.save()	# 수정된 내용대로 저장. 쿼리실행
        return super(PostDV, self).form_valid(form)


   


class PostAV(ArchiveIndexView):
    model = Post
    date_field = 'modify_dt'

class PostYAV(YearArchiveView):
    model =Post
    date_field = 'modify_dt'
    make_object_list= True

class PostMAV(MonthArchiveView) :
    model = Post
    date_field = 'modify_dt'

class PostDAV(DayArchiveView):
    model = Post
    date_field = 'modify_dt'

class PostTAV(TodayArchiveView):
    model=Post
    date_field = 'modify_dt'

class TagCloudTV(TemplateView):
    template_name = 'taggit/taggit_cloud.html'

class TaggedObjectLV(ListView):
    template_name = 'taggit/taggit_post_list.html'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(tags__name=self.kwargs.get('tag'))
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['tagname']= self.kwargs['tag']
        return context


class SearchFormView(FormView, ListView):
    model = Post.objects.filter(category='D')
    form_class= PostSearchForm
    template_name= 'domestic/post_domestic_search.html'
    context_object_name = 'posts'
    paginate_by=20
    success_url=reverse_lazy('domestic:search')
    


    def get_queryset(self):
        query = self.request.GET.get("search_word")

        if query:
            return Post.objects.filter(category='D').filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()

        return Post.objects.filter(category='D')


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['search_word']= self.request.GET.get("search_word")
        return context


class PostCreateView(CustomLoginRequiredMixin, CreateView):
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
    model= Post
    template_name='domestic/post_domestic_form.html'
    fields= ['title', 'content', 'tags']
    success_url = reverse_lazy('domestic:index')

class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model =Post
    template_name='domestic/post_domestic_confirm_delete.html'
    success_url = reverse_lazy('domestic:index')


class CommentDeleteView( DeleteView):
    model =PostComment
    def get_success_url(self):
        return reverse('domestic:post_detail', 
                       args=[self.object.blogpost_connected.id])