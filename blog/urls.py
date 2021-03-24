from django.urls import path, re_path
from blog import views


app_name = 'blog'
urlpatterns = [

    #Example: /blog/
    path('',views.PostLV.as_view(), name= 'index'),

    #/blog/tag/
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tag_foreign/', views.ForeignTagCloudTV.as_view(), name='tag_cloud_foreign')

    #/blog/tag/tagname/
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
    
    #Example: /blog/post/ (same as /blog/)
    path('post/', views.PostLV.as_view(), name='post_list'),

    #/blog/post/django-example/
    path('post/<int:pk>', views.PostDV.as_view(), name='post_detail'),

    #/blog/archive/
    path('archive/', views.PostAV.as_view(), name='post_archive'),

    #/blog/archive/2019/
    path('archive/<int:year>/', views.PostYAV.as_view(), name='post_year_archive'),

    #/blog/archive/2019/nov
    path('archive/<int:year>/<str:month>/', views.PostMAV.as_view(), name='post_month_archive'),

    #/blog/archive/2019/nov/10/
    path('archive/<int:year>/,<str:month>/<int:day>/', views.PostDAV.as_view(), name='post_day_archive'),

    #/blog/archive/today/
    path('archive/today/', views.PostTAV.as_view(), name='post_today_archive'),

    path('search/', views.SearchFormView.as_view(), name='search'),

    path('add/',views.PostCreateView.as_view(), name="add",),
    path('change/', views.PostChangeLV.as_view(), name="change",),
    
    path('update/<int:pk>/', views.PostUpdateView.as_view(), name="update",),
    path('<int:pk>/delete/', views.PostDeleteView.as_view(), name="delete",),
    path('comment/<int:pk>/delete/', views.CommentDeleteView.as_view(), name="comment_delete",),
    re_path(r'^owner/(?P<owner>[-\w]+)/(?P<owner_name>[-\w\s]+)$', views.PostUserLV.as_view(), name="post_user",),
    
    #인기글
    path('popular/', views.PostPopularLV.as_view(), name='popular_index'),
    path('popular/<int:pk>', views.PostPopularDV.as_view(), name='post_popular_detail'),
    path('blogpostpopular-like/<int:pk>', views.PostPopularLike, name="blogpost_popular_like"),
    #좋아요 눌렀을 때 가는 곳
    path('blogpost-like/<int:pk>', views.PostLike, name="blogpost_like"),
]  