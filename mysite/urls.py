"""mysite URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include,re_path
from mysite.views import KakaoSignInCallBackView,HomeView, SearchFormView, KakaoSignInView
from mysite.views import UserCreateDoneTV, SignUp, ProfileView, ActivateAccount,Ads
from django.conf.urls.static import static
from mysite import settings
from froala_editor import views
from .views import CustomLoginView

urlpatterns = [

    path('admin/', admin.site.urls),
    path('foreign/', include('blog.urls')),
    path('domestic/',include('domestic.urls')),
    path('', HomeView.as_view(), name= 'home'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/register/', SignUp.as_view(), name='register'),
    path('accounts/register/done/', UserCreateDoneTV.as_view(), name='register_done'),
    path('accounts/<int:pk>/', ProfileView.as_view(), name='profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('login/', CustomLoginView.as_view(template_name='registration/login.html'), name='login'),
    path('search/', SearchFormView.as_view(), name='search'),
    path('free/', include('free.urls')),
    path('froala_editor/',include('froala_editor.urls')),
    path('account/', include('allauth.urls')),
    path('kakaologin/', KakaoSignInView.as_view(), name='kakao'),
    path('users/signin/kakao/callback/', KakaoSignInCallBackView.as_view(), name='kakaoback'),
    path('app-ads.txt',Ads),
] #+  static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
