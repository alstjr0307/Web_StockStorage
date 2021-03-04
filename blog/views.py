
from django.views.generic import ListView, DetailView, TemplateView
from django.views.generic.dates import ArchiveIndexView, YearArchiveView, MonthArchiveView
from django.views.generic.dates import DayArchiveView, TodayArchiveView
from django.conf import settings
from django.views.generic import FormView
from blog.forms import PostSearchForm, PostForm
from django.db.models import Q
from django.shortcuts import render
from django.views.generic import CreateView, UpdateView, DeleteView
from django.contrib import messages
from mysite.forms import CustomLoginRequiredMixin, NewCommentForm
from django.urls import reverse_lazy
from mysite.views import OwnerOnlyMixin
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse
from blog.models import Post, PostComment
from mysite.views import FilteredListView
from django.views.generic.list import MultipleObjectMixin
from django.shortcuts import get_object_or_404
from hitcount.views import HitCountDetailView
from django.views.generic.edit import FormMixin
from django.http import HttpResponseRedirect
# Create your views here.

class PostLV(ListView,FormView):
    form_class= PostSearchForm
    model = Post
    template_name = 'blog/post_all.html'
    context_object_name = 'posts'
    paginate_by=20
    def get_queryset(self):
        return Post.objects.filter(category='F')

class PostDV(HitCountDetailView, FormView, MultipleObjectMixin,FormMixin):
    model=Post
    template_name='blog/post_detail.html'
    paginate_by = 20
    count_hit = True
    form_class=NewCommentForm
    


    def get_success_url(self):	# post처리가 성공한뒤 행할 행동
        return reverse('blog:post_detail', kwargs={'pk': self.object.pk})
    def get_queryset(self):
        return Post.objects.filter(category='F')
    def get_context_data(self, **kwargs):
        self.object_list = self.get_queryset()
        context = super().get_context_data(**kwargs)
       
        #댓글 기능 구현
        comments_connected = PostComment.objects.filter(blogpost_connected=self.get_object()).order_by('created')   
        context['comments'] = comments_connected
        context['user'] = self.request.user
        context['posts'] = Post.objects.filter(category='D')
        if self.request.user.is_authenticated:
            context['comment_form'] = '1'

        #좋아요 기능 구현
        likes_connected = get_object_or_404(Post, id=self.kwargs['pk'])
        liked = False
        if likes_connected.likes.filter(id=self.request.user.id).exists():
            liked = True
        context['number_of_likes'] = likes_connected.number_of_likes()
        context['post_is_liked'] = liked  

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
    
    model=Post.objects.filter(category='F')
    
    form_class= PostSearchForm
    template_name= 'blog/post_search.html'
    context_object_name='posts'
    paginate_by=20
    success_url=reverse_lazy('post:search')
    def get_queryset(self):
        query = self.request.GET.get("search_word")

        if query:
            return Post.objects.filter(category='F').filter(Q(title__icontains=query) | Q(content__icontains=query)).distinct()

        return Post.objects.filter(category='F')


    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['search_word']= self.request.GET.get("search_word")
        return context

class PostCreateView(CustomLoginRequiredMixin, CreateView):
    model =Post
    form_class=PostForm

    permission_denied_message='로그인이 필요합니다.'

    def get_initial(self):
        # Get the initial dictionary from the superclass method
        initial = super(PostCreateView,self).get_initial()
    # Copy the dictionary so we don't accidentally change a mutable dict
        initial = initial.copy()
        initial['category'] = 'F'
       # etc...
        return initial

    def get_success_url(self):
        return reverse('blog:post_detail', 
                       args=[self.object.pk])

    def form_valid(self, form):
        form.instance.owner = self.request.user
        return super().form_valid(form)
  
class PostChangeLV(CustomLoginRequiredMixin, ListView):
    template_name= 'blog/post_change_list.html'

    def get_queryset(self):
        return Post.objects.filter(owner=self.request.user)

class PostUpdateView(OwnerOnlyMixin, UpdateView):
    model= Post
    fields= ['title', 'content', 'tags']
    def get_success_url(self):
        return reverse('blog:post_detail', 
                       args=[self.object.pk])


class PostDeleteView(OwnerOnlyMixin, DeleteView):
    model =Post
    success_url = reverse_lazy('blog:index')

class CommentDeleteView( DeleteView):
    model =PostComment
    def get_success_url(self):
        return reverse('blog:post_detail', 
                       args=[self.object.blogpost_connected.id])
    
class PostUserLV(ListView):

    template_name= 'blog/post_user.html'
    context_object_name = 'posts'
    paginate_by=10
    
    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['owner_name']=self.kwargs['owner_name']
        context['owner']= self.kwargs['owner']  
        return context

    def get_queryset(self):
        return Post.objects.filter(owner=self.kwargs.get('owner'))

def PostLike(request, pk):
    post = get_object_or_404(Post, id=request.POST.get('blogpost_id'))
    if post.likes.filter(id=request.user.id).exists():
        post.likes.remove(request.user)
    else:
        post.likes.add(request.user)

    return HttpResponseRedirect(reverse('blog:post_detail', args=[str(pk)]))