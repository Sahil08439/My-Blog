"""
URL configuration for project1 project.

The urlpatterns list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path
from myblogs import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name='home'),
    path('contact/', views.Contact, name='contact'),
    path('Support', views.Support, name='Support'),
    path('newslatter/', views.subscription, name ='newslatter'),
    path('Blog/',views.blog,name='Blog'),
    path('ck',views.ck,name='ck'),
    path('allblogs', views.allblogs,name ='allblogs'),
    path('blog_details/<str:blog_id>/',views.blog_details,name ='blog_details'),
    path('loginuser', views.loginuser, name='loginuser'),
    path('signupuser',views.signupuser,name='signupuser'),
    path('logoutuser',views.logoutuser,name='logoutuser'),
    path('cat/<str:cat_id>/', views.cat, name='cat'),
    path('add_like/<str:blog_id>/', views.add_like, name='add_like'),
    path('add_comment/<str:blog_id>/',views.add_comment, name='add_comment'),
    path('delete_comment/<int:blog_id>/<int:comment_id>/',views.delete_comment, name='delete_comment'),
    path('edit_comment/<int:blog_id>/<int:comment_id>/', views.edit_comment, name='edit_comment'),
    path('findproduct', views.findproduct, name='findproduct'),
]

if settings.DEBUG:
        urlpatterns += static(settings.MEDIA_URL,
                              document_root=settings.MEDIA_ROOT)