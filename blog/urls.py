from django.urls import path, re_path
from blog import views


app_name = 'blog'
urlpatterns = [

    #Example: /blog/
    path('',views.PostLV.as_view(), name= 'index'),

    #/blog/tag/
    path('tag/', views.TagCloudTV.as_view(), name='tag_cloud'),
    path('tagforeign/', views.ForeignTagCloudTV.as_view(), name='tag_cloud_foreign'),

    #/blog/tag/tagname/
    path('tag/<str:tag>/', views.TaggedObjectLV.as_view(), name='tagged_object_list'),
    path('tagforeign/<str:tag>/', views.ForeignTaggedObjectLV.as_view(), name='tagged_object_list_foreign'),
    #Example: /blog/post/ (same as /blog/)
    path('post/', views.PostLV.as_view(), name='post_list'),

    #/blog/post/django-example/
    path('post/<int:pk>', views.PostDV.as_view(), name='post_detail'),

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