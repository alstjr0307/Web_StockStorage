from django.db import models
from django.urls import reverse
from taggit.managers import TaggableManager
from django.contrib.auth.models import User
from django.utils.text import slugify
from froala_editor.fields import FroalaField

class Post(models.Model):
    title = models.CharField(verbose_name='제목', max_length=50)
    slug = models.SlugField('SLUG', allow_unicode=True, help_text='one word for title alias.')
    description = models.CharField('DESCRIPTION', max_length=100, blank=True, help_text='simple description text.')
    content = FroalaField('CONTENT', blank=False)
    create_dt = models.DateTimeField('CREATE DATE', auto_now_add=True)
    modify_dt= models.DateTimeField('MODIFY DATE', auto_now=True)
    tags= TaggableManager('태그',blank=True)
    owner =models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='작성자', blank=True, null=True)
    Category_CHOICES=(('F','해외주식'),('D', '국내주식'))
    category=models.CharField(verbose_name='게시판', max_length=1, choices=Category_CHOICES, default='F' )

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
        


# Create your models here.
