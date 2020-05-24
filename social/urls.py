# """dj2django URL Configuration
#
# The `urlpatterns` list routes URLs to views. For more information please see:
#     https://docs.djangoproject.com/en/3.0/topics/http/urls/
# Examples:
# Function views
#     1. Add an import:  from my_app import views
#     2. Add a URL to urlpatterns:  path('', views.home, name='home')
# Class-based views
#     1. Add an import:  from other_app.views import Home
#     2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
# Including another URLconf
#     1. Import the include() function: from django.urls import include, path
#     2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
# """
from django.contrib import admin
from django.urls import path

from social import views
from django.views.generic import RedirectView

from social.views import ContactView, AboutView, HomeView, MyProfileUpdateView, MyPostCreate, MyPostListView, \
    MyPostDetailView, MyProfileListView, MyPostDeleteView, MyProfileDetailView

urlpatterns = [
    path('home/', HomeView.as_view()),
    path('about/', AboutView.as_view()),
    path('contact/', ContactView.as_view()),
    # path('mylist/',MyList.as_view()),
    path('mypost/create/', MyPostCreate.as_view(success_url="/social/mypost")),
    path('mypost/delete/<int:pk>', MyPostDeleteView.as_view(success_url="/social/mypost")),
    path('mypost/<int:pk>', MyPostDetailView.as_view()),
    path('mypost/', MyPostListView.as_view()),
    path('myprofile/edit/<int:pk>/', MyProfileUpdateView.as_view(success_url="/social/home/")),
    path('', RedirectView.as_view(url='home/')),

    path('myprofile/', MyProfileListView.as_view()),
    path('myprofile/<int:pk>', MyProfileDetailView.as_view()),

    path("myprofile/follow/<int:pk>/", views.follow),

]
