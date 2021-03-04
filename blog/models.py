from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify
from froala_editor.fields import FroalaField
from datetime import datetime, timedelta
from django.utils import timezone

from hitcount.models import HitCountMixin, HitCount
from django.contrib.contenttypes.fields import GenericRelation


class Post(models.Model):
    title = models.CharField(verbose_name='제목', max_length=40)
    slug = models.SlugField('SLUG', allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = models.CharField('CONTENT', max_length=10000000000000,blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt= models.DateTimeField('MODIFY DATE', auto_now=True)
    tags= TaggableManager('태그',blank=True)
    owner =models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자', blank=True, null=True)
    Category_CHOICES=(('F','해외주식'),('D', '국내주식'))
    category=models.CharField(verbose_name='게시판', max_length=1, choices=Category_CHOICES, default='F' )
    hit_count_generic = GenericRelation(HitCount, object_id_field='object_pk',
     related_query_name='hit_count_generic_relation')
    likes = models.ManyToManyField(User, related_name='blogpost_like')

    class Meta:
        verbose_name = 'post'
        verbose_name_plural = 'posts'
        db_table = 'blog_posts'
        ordering=('-create_dt',)
    
    def __str__(self):
        return self.title
    
    def owner_absolute_url(self):
        return reverse('blog:post_user', args=(self.owner.id, self.owner.first_name))
    def get_absolute_url(self):
        if self.category=="F":

            return reverse('blog:post_detail', args=(self.id,))
        
        if self.category=="D":

            return reverse('domestic:post_detail', args=(self.id,))
    
    def get_previous(self):
        return self.get_previous_by_modify_dt()
    def get_next(self):
        return self.get_next_by_modify_dt()

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title, allow_unicode=True)
        super().save(*args, **kwargs)

    def created_string(self):
        
        time = datetime.now(timezone.utc) - self.create_dt

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.create_dt.date()
            return str(time.days) + '일전'
        else:
            return False        

    @property
    def number_of_comments(self):
        return PostComment.objects.filter(blogpost_connected=self).count()


    @property
    def update_counter(self):
        self.n_hit = self.n_hit+1
        self.save()

    def number_of_likes(self):
        return self.likes.count()
        
class PostComment(models.Model):
    blogpost_connected= models.ForeignKey(Post, related_name='comments', on_delete=models.CASCADE)
    writer=models.ForeignKey(User, on_delete=models.CASCADE)
    content= models.TextField()
    created= models.DateTimeField(auto_now_add=True)
    updated=models.DateTimeField(auto_now=True)

    class Meta: ordering=['created']

    def created_string(self):
        
        time = datetime.now(timezone.utc) - self.created

        if time < timedelta(minutes=1):
            return '방금 전'
        elif time < timedelta(hours=1):
            return str(int(time.seconds / 60)) + '분전'
        elif time < timedelta(days=1):
            return str(int(time.seconds / 3600)) + '시간전'
        elif time < timedelta(days=7):
            time = datetime.now(tz=timezone.utc).date() - self.created.date()
            return str(time.days) + '일전'
        else:
            return False        